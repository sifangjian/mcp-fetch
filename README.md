# mcp-fetch - MCP Fetch

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)  [![MCP](https://img.shields.io/badge/MCP-1.0.0-green.svg)](https://modelcontextprotocol.io/)  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*基于 MCP 协议的 HTTP 请求工具 - 让 AI 助手轻松调用 REST API*

[English](./README_en.md) | 简体中文(./README.md)

</div>

## 简介

一个 Model Context Protocol (MCP) 服务器，提供 HTTP 请求工具用于调用本地或远程 REST API 服务。

这个 MCP 服务器暴露了一个 `http_request` 工具，使 AI 助手能够在测试、验证和数据获取工作流程中与 REST API 进行交互。它专为希望测试 API 或将外部服务集成到 AI 工作流程中的开发者设计。

## 功能特点

- **多种 HTTP 方法**：支持 GET、POST、PUT、DELETE 和 PATCH 请求
- **自定义请求头**：传递自定义 HTTP 头用于认证或内容协商
- **请求体**：发送 JSON 或原始内容
- **可配置超时**：为长时间运行的请求设置自定义超时时间
- **错误处理**：为超时、连接失败等问题提供全面的错误信息
- **异步操作**：基于 httpx 构建，支持完整异步操作

## 安装

### 环境要求

- Python 3.11 或更高版本
- pip 或 uv 包管理器

### 使用 uv（推荐）

```bash
uv pip install -e .
```

### 使用 pip

```bash
pip install -e .
```

## 使用方法

### 作为 MCP 服务器

此服务器旨在与 MCP 兼容的 AI 助手或客户端配合使用。配置您的 MCP 客户端使用此服务器：

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

### 在开发工具中配置

在您的开发工具（如 VS Code、Trae 等 MCP 客户端）中配置此服务器：

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

### 直接运行

```bash
python server.py
```

## 工具：http_request

向本地或远程服务发送 HTTP 请求。

### 参数

| 参数      | 类型          | 必填 | 默认值 | 说明                                                        |
| --------- | ------------- | ---- | ------ | ----------------------------------------------------------- |
| `url`     | string        | 是   | -      | 请求的完整 URL（例如 `http://localhost:8080/api/endpoint`） |
| `method`  | string        | 否   | GET    | HTTP 方法（GET, POST, PUT, DELETE, PATCH）                  |
| `headers` | object        | 否   | {}     | HTTP 请求头，键值对形式                                     |
| `body`    | object/string | 否   | null   | 请求体（用于 POST/PUT/PATCH）                               |
| `timeout` | number        | 否   | 30     | 请求超时时间（秒）                                          |

### 响应格式

```json
{
  "status_code": 200,
  "headers": {...},
  "body": "响应内容",
  "is_success": true
}
```

### 错误格式

```json
{
  "error": "错误描述",
  "url": "请求的 URL",
  "method": "HTTP 方法"
}
```

## 使用示例

### GET 请求

```python
{
  "url": "http://localhost:3000/api/users",
  "method": "GET"
}
```

### POST 请求（带 JSON body）

```python
{
  "url": "http://localhost:3000/api/users",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer token123"
  },
  "body": {
    "name": "张三",
    "email": "zhangsan@example.com"
  }
}
```

### DELETE 请求

```python
{
  "url": "http://localhost:3000/api/users/123",
  "method": "DELETE"
}
```

## 开发

### 设置开发环境

```bash
# 以可编辑模式安装包
uv pip install -e .

# 或安装开发依赖
uv pip install -e ".[dev]"
```

### 项目结构

```
mcp-fetch/
├── server.py          # MCP 服务器主要实现
├── main.py            # 入口文件
├── pyproject.toml     # 项目配置
└── README.md          # 说明文档
```

## 依赖

- [mcp](https://github.com/modelcontextprotocol/python-sdk) >= 1.0.0 - Model Context Protocol SDK
- [httpx](https://www.python-httpx.org/) >= 0.27.0 - 异步 HTTP 客户端

## 开源协议

MIT License

## 贡献

欢迎提交 Pull Request！