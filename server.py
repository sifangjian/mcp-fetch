"""
MCP Fetch - A Model Context Protocol tool for calling local or remote REST API services
"""

import json
from typing import Any
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("mcp-fetch")

TOOL_DEFINITION = Tool(
    name="http_request",
    description="Makes an HTTP request to a local or remote service. Use this tool when you need to call REST API endpoints for testing, verification, or data retrieval.",
    inputSchema={
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The full URL of the request (e.g., http://localhost:8080/api/endpoint)"
            },
            "method": {
                "type": "string",
                "description": "HTTP method (GET, POST, PUT, DELETE, PATCH)",
                "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
                "default": "GET"
            },
            "headers": {
                "type": "object",
                "description": "HTTP headers as key-value pairs",
                "additionalProperties": {"type": "string"},
            },
            "body": {
                "type": ["object", "string", "null"],
                "description": "Request body (for POST/PUT/PATCH). Will be JSON encoded if object."
            },
            "timeout": {
                "type": "number",
                "description": "Request timeout in seconds",
                "default": 30
            }
        },
        "required": ["url"]
    }
)

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [TOOL_DEFINITION]

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name != "http_request":
        raise ValueError(f"Unknown tool: {name}")

    url = arguments["url"]
    method = arguments.get("method", "GET").upper()
    headers = arguments.get("headers", {})
    body = arguments.get("body", None)
    timeout = arguments.get("timeout", 30)

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            if method == "GET":
                response = await client.get(url, headers=headers)
            elif method == "POST":
                if isinstance(body, dict):
                    response = await client.post(url, headers=headers, json=body)
                else:
                    response = await client.post(url, headers=headers, content=body)
            elif method == "PUT":
                if isinstance(body, dict):
                    response = await client.put(url, headers=headers, json=body)
                else:
                    response = await client.put(url, headers=headers, content=body)
            elif method == "DELETE":
                response = await client.delete(url, headers=headers)
            elif method == "PATCH":
                if isinstance(body, dict):
                    response = await client.patch(url, headers=headers, json=body)
                else:
                    response = await client.patch(url, headers=headers, content=body)
            else:
                return [TextContent(
                    type="text",
                    text=f"Error: Unsupported HTTP method '{method}'"
                )]

            result = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response.text,
                "is_success": 200 <= response.status_code < 300
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except httpx.TimeoutException:
        return [TextContent(type="text", text=json.dumps({
            "error": "Request timed out",
            "url": url,
            "method": method
        }, indent=2))]
    except httpx.ConnectError as e:
        return [TextContent(type="text", text=json.dumps({
            "error": f"Connection failed: {str(e)}",
            "url": url,
            "method": method
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "error": str(e),
            "url": url,
            "method": method
        }, indent=2))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())