# mcp-fetch

A Model Context Protocol (MCP) server that provides an HTTP request tool for calling local or remote REST API services.

## Overview

This MCP server exposes an `http_request` tool that enables AI assistants to interact with REST APIs during testing, verification, and data retrieval workflows. It's designed for developers who want to test APIs or integrate external services into their AI-powered workflows.

## Features

- **Multiple HTTP Methods**: Supports GET, POST, PUT, DELETE, and PATCH requests
- **Custom Headers**: Pass custom HTTP headers for authentication or content negotiation
- **Request Body**: Send JSON or raw body content with requests
- **Configurable Timeout**: Set custom timeout values for long-running requests
- **Error Handling**: Comprehensive error messages for timeouts, connection failures, and other issues
- **Async Operations**: Built on httpx for full async support

## Installation

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager

### Using uv (Recommended)

```bash
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

## Usage

### As an MCP Server

This server is designed to be used with an MCP-compatible AI assistant or client. Configure your MCP client to use this server:

```json
{
  "mcpServers": {
    "mcp-fetch": {
      "command": "python",
      "args": ["-m", "mcp_fetch"]
    }
  }
}
```

### Running Directly

```bash
python server.py
```

## Tool: http_request

Makes an HTTP request to a local or remote service.

### Parameters

| Parameter | Type          | Required | Default | Description                                                              |
| --------- | ------------- | -------- | ------- | ------------------------------------------------------------------------ |
| `url`     | string        | Yes      | -       | The full URL of the request (e.g., `http://localhost:8080/api/endpoint`) |
| `method`  | string        | No       | GET     | HTTP method (GET, POST, PUT, DELETE, PATCH)                              |
| `headers` | object        | No       | {}      | HTTP headers as key-value pairs                                          |
| `body`    | object/string | No       | null    | Request body (for POST/PUT/PATCH)                                        |
| `timeout` | number        | No       | 30      | Request timeout in seconds                                               |

### Response Format

```json
{
  "status_code": 200,
  "headers": {...},
  "body": "response content",
  "is_success": true
}
```

### Error Format

```json
{
  "error": "Error description",
  "url": "requested URL",
  "method": "HTTP method"
}
```

## Examples

### GET Request

```python
{
  "url": "http://localhost:3000/api/users",
  "method": "GET"
}
```

### POST Request with JSON Body

```python
{
  "url": "http://localhost:3000/api/users",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer token123"
  },
  "body": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### DELETE Request

```python
{
  "url": "http://localhost:3000/api/users/123",
  "method": "DELETE"
}
```

## Development

### Setup Development Environment

```bash
# Install the package in editable mode
uv pip install -e .

# Or with dev dependencies
uv pip install -e ".[dev]"
```

### Project Structure

```
mcp-fetch/
├── server.py          # Main MCP server implementation
├── main.py            # Entry point
├── pyproject.toml     # Project configuration
└── README.md          # This file
```

## Dependencies

- [mcp](https://github.com/modelcontextprotocol/python-sdk) >= 1.0.0 - Model Context Protocol SDK
- [httpx](https://www.python-httpx.org/) >= 0.27.0 - Async HTTP client

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
