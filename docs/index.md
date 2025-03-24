# NetBox MCP Server

A Model Context Protocol (MCP) server implementation for NetBox integration, enabling AI agents to interact with NetBox infrastructure data.

## Overview

The NetBox MCP Server provides a standardized interface for AI agents to query and manage network infrastructure data stored in NetBox. It implements the Model Context Protocol, making it easy for AI assistants to:

- Query device information
- Manage IP addresses and prefixes
- Access site and rack data
- Search across NetBox objects
- Perform complex infrastructure queries

## Features

- **Complete NetBox API Coverage**: Access to all NetBox object types and operations
- **MCP Compliance**: Full implementation of the Model Context Protocol
- **Robust Error Handling**: Comprehensive error handling and recovery mechanisms
- **Type Safety**: Strong typing and parameter validation
- **Extensible**: Easy to extend with new capabilities
- **Well Tested**: Comprehensive test suite with high coverage

## Quick Links

- [Installation Guide](getting-started/installation.md)
- [Quick Start](getting-started/quickstart.md)
- [API Reference](api/netbox-client.md)
- [Contributing Guide](development/contributing.md)

## Requirements

- Python 3.8+
- NetBox instance (self-hosted or NetBox Cloud)
- NetBox API token with appropriate permissions

## Installation

```bash
pip install netbox-mcp-server
```

For development installation:

```bash
git clone https://github.com/yourusername/netbox-mcp-server
cd netbox-mcp-server
pip install -e ".[test,docs]"
```

## Basic Usage

```python
from netbox_mcp import NetBoxMCPServer

# Initialize the server
server = NetBoxMCPServer(
    url="https://netbox.example.com",
    token="your_api_token"
)

# Start the server
server.run()
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](development/contributing.md) for details. 