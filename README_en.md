# mcp-fetch

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)  [![MCP](https://img.shields.io/badge/MCP-1.0.0-green.svg)](https://modelcontextprotocol.io/)  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*HTTP Request Tool Based on MCP Protocol - Enabling AI Assistants to Easily Invoke REST APIs*

[English](./README_en.md) | [简体中文](./README.md)

</div>

## Overview

A Model Context Protocol (MCP) server that provides an HTTP request tool for calling local or remote REST API services.

This MCP server exposes an `http_request` tool that enables AI assistants to interact with REST APIs during testing, verification, and data retrieval workflows. It's designed for developers who want to test APIs or integrate external services into their AI-powered workflows.

## Features

- **Multiple HTTP Methods**: Supports GET, POST, PUT, DELETE, and PATCH requests
- **Custom Headers**: Pass custom HTTP headers for authentication or content negotiation
- **Request Body**: Send JSON or raw body content with requests
- **File Upload**: Supports multipart/form-data format for file uploads
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

### In Development Tools

Configure this server in your development tools (such as VS Code, Trae, or other MCP clients):

```json
{
  "mcpServers": {
    "mcp-fetch": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "server.py"
      ],
      "cwd": "f:\\workspace\\python\\mcp-fetch"
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

| Parameter  | Type          | Required | Default | Description                                                              |
| ---------- | ------------- | -------- | ------- | ------------------------------------------------------------------------ |
| `url`      | string        | Yes      | -       | The full URL of the request (e.g., `http://localhost:8080/api/endpoint`) |
| `method`   | string        | No       | GET     | HTTP method (GET, POST, PUT, DELETE, PATCH)                              |
| `headers`  | object        | No       | {}      | HTTP headers as key-value pairs                                          |
| `body`     | object/string | No       | null    | Request body (for POST/PUT/PATCH)                                        |
| `files`    | object        | No       | null    | Files to upload via multipart/form-data format                           |
| `form_data` | object      | No       | null    | Additional form fields for multipart requests                            |
| `timeout`  | number        | No       | 30      | Request timeout in seconds                                               |

### files Parameter Structure

The `files` parameter is an object where keys are form field names and values can be a single file object or an array of file objects.

**Single file object structure:**

```json
{
  "filename": "example.txt",
  "content_type": "text/plain",
  "content": "File content (Base64 encoded or raw string)"
}
```

**File array structure (for multiple files in the same field):**

```json
[
  {
    "filename": "file1.txt",
    "content_type": "text/plain",
    "content": "First file content"
  },
  {
    "filename": "file2.txt",
    "content_type": "text/plain",
    "content": "Second file content"
  }
]
```

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

### File Upload (Single File)

```python
{
  "url": "http://localhost:3000/api/upload",
  "method": "POST",
  "files": {
    "file": {
      "filename": "document.pdf",
      "content_type": "application/pdf",
      "content": "Base64-encoded file content..."
    }
  }
}
```

### File Upload (Multiple Files)

```python
{
  "url": "http://localhost:3000/api/upload",
  "method": "POST",
  "files": {
    "documents": [
      {
        "filename": "file1.txt",
        "content_type": "text/plain",
        "content": "First file content"
      },
      {
        "filename": "file2.txt",
        "content_type": "text/plain",
        "content": "Second file content"
      }
    ]
  }
}
```

### File Upload with Form Fields

```python
{
  "url": "http://localhost:3000/api/upload",
  "method": "POST",
  "files": {
    "file": {
      "filename": "avatar.png",
      "content_type": "image/png",
      "content": "Base64-encoded image content..."
    }
  },
  "form_data": {
    "description": "User avatar",
    "category": "profile"
  }
}
```

### PUT Request with File Upload

```python
{
  "url": "http://localhost:3000/api/documents/123",
  "method": "PUT",
  "files": {
    "document": {
      "filename": "updated_file.pdf",
      "content_type": "application/pdf",
      "content": "Updated file content..."
    }
  }
}
```

### PATCH Request with File Upload

```python
{
  "url": "http://localhost:3000/api/users/456/avatar",
  "method": "PATCH",
  "files": {
    "avatar": {
      "filename": "new_avatar.jpg",
      "content_type": "image/jpeg",
      "content": "Base64-encoded image content..."
    }
  }
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
└── README.md          # Documentation
```

## Dependencies

- [mcp](https://github.com/modelcontextprotocol/python-sdk) >= 1.0.0 - Model Context Protocol SDK
- [httpx](https://www.python-httpx.org/) >= 0.27.0 - Async HTTP client

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
