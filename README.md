# NetBox MCP Server

This is a [Model Context Protocol](https://modelcontextprotocol.io/) server for NetBox. It enables you to interact with your data in NetBox directly via LLMs that support MCP, with both read and write capabilities.

## Tools

| Tool | Description |
|------|-------------|
| get_objects | Retrieves NetBox core objects based on their type and filters |
| search_netbox | Performs a global search across NetBox objects |
| get_object_by_id | Gets detailed information about a specific NetBox object by its ID |
| create_object | Creates a new object in NetBox |
| update_object | Updates an existing object in NetBox |
| delete_object | Deletes an object from NetBox |
| bulk_create_objects | Creates multiple objects in NetBox in a single API call |
| bulk_update_objects | Updates multiple objects in NetBox in a single API call |
| bulk_delete_objects | Deletes multiple objects from NetBox in a single API call |

> Note: the set of supported object types is explicitly defined and limited to the core NetBox objects for now, and won't work with object types from plugins.

## Usage

1. Create an API token in NetBox with appropriate permissions:
   - Read-only if you only need read operations
   - Read-write if you need write operations

2. Install dependencies: `uv add -r requirements.txt`

3. Verify the server can run: `NETBOX_URL=https://netbox.example.com/ NETBOX_TOKEN=<your-api-token> uv run server.py`

3. Add the MCP server configuration to your LLM client.  For example, in Claude Desktop (Mac):

```json
{
  "mcpServers": {
        "netbox": {
            "command": "uv",
            "args": [
                "--directory",
                "/path/to/netbox-mcp-server",
                "run",
                "server.py"
            ],
            "env": {
                "NETBOX_URL": "https://netbox.example.com/",
                "NETBOX_TOKEN": "<your-api-token>"
            }
        }
}
```
> On Windows, use full, escaped path to your instance, such as `C:\\Users\\myuser\\.local\\bin\\uv` and `C:\\Users\\myuser\\netbox-mcp-server`. 
> For detailed troubleshooting, consult the [MCP quickstart](https://modelcontextprotocol.io/quickstart/user).

4. Use the tools in your LLM client.  For example:

```text
> Get all devices in the 'Equinix DC14' site
...
> Tell me about my IPAM utilization
...
> What Cisco devices are in my network?
...
> Create a new device called "new-server" with device type ID 5, role ID 3, and site ID 1
...
> Update device 123 to change its status to "planned"
...
> Delete IP address with ID 456
```

## Security Notes

When using write operations, consider the following:

1. Use the least privileged API token possible for your needs. If you only need read access, use a read-only token.
2. Be aware that write operations can modify or delete data in your NetBox instance. Use caution when granting write access.
3. Consider implementing additional audit logging when using write operations.
4. Test write operations in a non-production environment before using them in production.

For detailed documentation on each tool, see the [API Reference](README-client.md#api-reference).

## Development

Contributions are welcome!  Please open an issue or submit a PR.

## License

This project is licensed under the Apache 2.0 license.  See the LICENSE file for details.
