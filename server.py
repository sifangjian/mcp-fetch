"""
MCP Fetch - A Model Context Protocol tool for calling local or remote REST API services

This module provides an MCP server that exposes an HTTP request tool, enabling AI assistants
to interact with REST APIs for testing, verification, and data retrieval workflows.
"""

import json
from typing import Any, Union
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Initialize the MCP server with the name "mcp-fetch"
server = Server("mcp-fetch")

# Tool input schema property definitions for multipart form data fields
_FORM_FILE_PROPERTY = {
    "type": "object",
    "description": "File to upload via multipart/form-data. Contains 'filename' and optional 'content_type'."
}

_FORM_FILE_ARRAY_PROPERTY = {
    "type": "array",
    "items": _FORM_FILE_PROPERTY,
    "description": "Array of files to upload via multipart/form-data."
}

_TOOL_DEFINITION = Tool(
    name="http_request",
    description="Makes an HTTP request to a local or remote service. Use this tool when you need to call REST API endpoints for testing, verification, or data retrieval. Supports file uploads via multipart/form-data.",
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
            "files": {
                "type": "object",
                "description": "Multipart file uploads. Keys are field names, values can be a single file object or array of file objects. Each file object should contain 'filename' (required), 'content_type' (optional, defaults to 'application/octet-stream'), and 'content' (required, can be string or bytes; strings will be UTF-8 encoded).",
                "additionalProperties": {
                    "anyOf": [_FORM_FILE_PROPERTY, _FORM_FILE_ARRAY_PROPERTY]
                },
            },
            "form_data": {
                "type": "object",
                "description": "Additional form fields to include in multipart requests.",
                "additionalProperties": {"type": "string"},
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
    """
    Expose the list of available tools to the MCP client.

    This function is called by the MCP protocol to discover available tools.
    Returns a list containing the http_request tool definition.
    """
    return [_TOOL_DEFINITION]


def _build_multipart_files(files: dict) -> dict:
    """
    Build the files dictionary for httpx multipart request from the input schema.

    Converts the simplified file schema (with filename, content_type, content)
    into the format expected by httpx's files parameter.

    Args:
        files: Dictionary mapping field names to file objects or arrays of file objects.
               Each file object should contain 'filename' and optionally 'content_type' and 'content'.

    Returns:
        Dictionary formatted for httpx multipart files parameter.
    """
    result = {}
    for field_name, file_spec in files.items():
        if isinstance(file_spec, list):
            result[field_name] = [
                {
                    "filename": f.get("filename", "upload"),
                    "content_type": f.get("content_type", "application/octet-stream"),
                    "content": _ensure_bytes(f.get("content", b"")),
                }
                for f in file_spec
            ]
        else:
            result[field_name] = {
                "filename": file_spec.get("filename", "upload"),
                "content_type": file_spec.get("content_type", "application/octet-stream"),
                "content": _ensure_bytes(file_spec.get("content", b"")),
            }
    return result


def _ensure_bytes(content: Union[str, bytes]) -> bytes:
    """
    Ensure content is converted to bytes.

    If content is a string, encode it to UTF-8 bytes.
    If content is already bytes, return as-is.

    Args:
        content: String or bytes content to convert.

    Returns:
        Content as bytes.
    """
    if isinstance(content, bytes):
        return content
    return content.encode("utf-8")


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """
    Execute the specified tool with the given arguments.

    This function is called by the MCP protocol when a client requests tool execution.
    It processes the HTTP request parameters and performs the actual HTTP call.

    Args:
        name: The name of the tool to execute (should be "http_request").
        arguments: Dictionary containing the tool arguments including url, method, headers, body, etc.

    Returns:
        List containing a TextContent object with the response or error information.

    Raises:
        ValueError: If an unknown tool name is provided.
    """
    if name != "http_request":
        raise ValueError(f"Unknown tool: {name}")

    # Extract HTTP request parameters from arguments
    url = arguments["url"]
    method = arguments.get("method", "GET").upper()
    headers = arguments.get("headers", {})
    body = arguments.get("body", None)
    files = arguments.get("files", None)
    form_data = arguments.get("form_data", None)
    timeout = arguments.get("timeout", 30)

    # Automatically prepend http:// if no protocol is specified
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            # Handle multipart file upload requests
            if files is not None:
                multipart_files = _build_multipart_files(files)
                multipart_data = form_data if form_data else {}

                if method == "POST":
                    response = await client.post(url, headers=headers, files=multipart_files, data=multipart_data)
                elif method == "PUT":
                    response = await client.put(url, headers=headers, files=multipart_files, data=multipart_data)
                elif method == "PATCH":
                    response = await client.patch(url, headers=headers, files=multipart_files, data=multipart_data)
                else:
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "error": f"File upload is only supported for POST, PUT, and PATCH methods. Got: '{method}'",
                            "url": url,
                            "method": method
                        }, indent=2)
                    )]

            # Handle standard GET request
            elif method == "GET":
                response = await client.get(url, headers=headers)

            # Handle POST request with JSON or raw body
            elif method == "POST":
                if isinstance(body, dict):
                    response = await client.post(url, headers=headers, json=body)
                else:
                    response = await client.post(url, headers=headers, content=body)

            # Handle PUT request with JSON or raw body
            elif method == "PUT":
                if isinstance(body, dict):
                    response = await client.put(url, headers=headers, json=body)
                else:
                    response = await client.put(url, headers=headers, content=body)

            # Handle DELETE request
            elif method == "DELETE":
                response = await client.delete(url, headers=headers)

            # Handle PATCH request with JSON or raw body
            elif method == "PATCH":
                if isinstance(body, dict):
                    response = await client.patch(url, headers=headers, json=body)
                else:
                    response = await client.patch(url, headers=headers, content=body)

            # Reject unsupported HTTP methods
            else:
                return [TextContent(
                    type="text",
                    text=f"Error: Unsupported HTTP method '{method}'"
                )]

            # Build standardized response object
            result = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response.text,
                "is_success": 200 <= response.status_code < 300
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

    # Handle request timeout gracefully
    except httpx.TimeoutException:
        return [TextContent(type="text", text=json.dumps({
            "error": "Request timed out",
            "url": url,
            "method": method
        }, indent=2))]

    # Handle connection errors (e.g., host not reachable)
    except httpx.ConnectError as e:
        return [TextContent(type="text", text=json.dumps({
            "error": f"Connection failed: {str(e)}",
            "url": url,
            "method": method
        }, indent=2))]

    # Catch-all for any other unexpected errors
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "error": str(e),
            "url": url,
            "method": method
        }, indent=2))]


async def main():
    """
    Main entry point for the MCP Fetch server.

    Initializes the stdio-based server transport and runs the MCP server loop.
    This function blocks indefinitely as the server processes incoming requests.
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
