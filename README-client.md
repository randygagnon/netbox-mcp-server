# NetBox Client Library

A Python client library for interacting with NetBox, providing both a base abstract class and a REST API implementation.

## Features

- Abstract base class with generic CRUD methods
- REST API implementation of the base class
- Support for both single and bulk operations
- Designed to be extensible for ORM-based implementations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### REST API Client

```python
from client import NetBoxRestClient

# Initialize the client
client = NetBoxRestClient(
    url="https://netbox.example.com",
    token="your_api_token_here",
    verify_ssl=True
)

# Get all sites
sites = client.get("dcim/sites")
print(f"Found {len(sites)} sites")

# Get a specific site
site = client.get("dcim/sites", id=1)
print(f"Site name: {site.get('name')}")

# Example with pagination
# Get sites page by page
page = 1
limit = 50
while True:
    sites_page = client.get("dcim/sites", params={
        "limit": limit,
        "offset": (page - 1) * limit
    })
    if not sites_page:
        break
        
    print(f"Processing page {page} with {len(sites_page)} sites")
    for site in sites_page:
        print(f"Site: {site.get('name')}")
        
    page += 1

# Create a new site
new_site = client.create("dcim/sites", {
    "name": "New Site",
    "slug": "new-site",
    "status": "active"
})
print(f"Created site: {new_site.get('name')} (ID: {new_site.get('id')})")

# Update a site
updated_site = client.update("dcim/sites", id=1, data={
    "description": "Updated description"
})

# Delete a site
success = client.delete("dcim/sites", id=1)
if success:
    print("Site deleted successfully")

# Bulk operations
new_sites = client.bulk_create("dcim/sites", [
    {"name": "Site 1", "slug": "site-1", "status": "active"},
    {"name": "Site 2", "slug": "site-2", "status": "active"}
])

updated_sites = client.bulk_update("dcim/sites", [
    {"id": 1, "description": "Updated description 1"},
    {"id": 2, "description": "Updated description 2"}
])

success = client.bulk_delete("dcim/sites", ids=[1, 2])
```

## Extending for ORM Implementation

The `NetBoxClientBase` abstract base class can be extended to create an ORM-based implementation for use within a NetBox plugin:

```python
from client import NetBoxClientBase
from django.db import transaction

class NetBoxOrmClient(NetBoxClientBase):
    """
    NetBox client implementation using the ORM directly.
    This would be used within a NetBox plugin.
    """
    
    def __init__(self):
        # No authentication needed as this would run within NetBox
        pass
    
    def get(self, endpoint, id=None, params=None):
        # Implementation would use Django ORM to fetch objects
        # Example (not implemented)
        pass
    
    # Other methods would be implemented similarly
```

## License

MIT

## API Reference

### Read Operations

#### get_objects

Get objects from NetBox based on their type and filters.

Arguments:

- `object_type`: String representing the NetBox object type (e.g. "devices", "ip-addresses")
- `filters`: Dict of filters to apply to the API call based on the NetBox API filtering options

Example:

```python
get_objects("devices", {"status": "active", "manufacturer_id": 1})
```

#### search_netbox

Perform a global search across NetBox objects.

Arguments:

- `query`: Search string to look for across NetBox objects
- `limit`: Maximum number of results to return (default: 10)

Example:

```python
search_netbox("server", 5)
```

#### get_object_by_id

Get detailed information about a specific NetBox object by its ID.

Arguments:

- `object_type`: String representing the NetBox object type (e.g. "devices", "ip-addresses")
- `object_id`: The numeric ID of the object

Example:

```python
get_object_by_id("devices", 123)
```

### Write Operations

#### create_object

Create a new object in NetBox.

Arguments:

- `object_type`: String representing the NetBox object type (e.g. "devices", "ip-addresses")
- `data`: Dictionary containing the object properties to create

Example - Creating a new device:

```python
create_object("devices", {
    "name": "new-device",
    "device_type": 1,
    "role": 1,
    "site": 1,
    "status": "active"
})
```

Example - Creating a new IP address:

```python
create_object("ip-addresses", {
    "address": "192.168.100.1/24",
    "status": "active",
    "description": "Example IP"
})
```

#### update_object

Update an existing object in NetBox.

Arguments:

- `object_type`: String representing the NetBox object type (e.g. "devices", "ip-addresses")
- `object_id`: The numeric ID of the object to update
- `data`: Dictionary containing the object properties to update

Example - Updating a device:

```python
update_object("devices", 123, {
    "name": "updated-device-name",
    "status": "planned"
})
```

Example - Updating an IP address:

```python
update_object("ip-addresses", 456, {
    "description": "Updated description",
    "status": "reserved"
})
```

#### delete_object

Delete an object from NetBox.

Arguments:

- `object_type`: String representing the NetBox object type (e.g. "devices", "ip-addresses")
- `object_id`: The numeric ID of the object to delete

Example:

```python
delete_object("devices", 123)
```

### Bulk Operations

#### bulk_create_objects

Create multiple objects in NetBox in a single API call.

Arguments:

- `object_type`: String representing the NetBox object type (e.g. "devices", "ip-addresses")
- `data_list`: List of dictionaries, each containing the properties for one object to create

Example - Creating multiple IP addresses:

```python
bulk_create_objects("ip-addresses", [
    {
        "address": "192.168.100.1/24",
        "status": "active",
        "description": "Example IP 1"
    },
    {
        "address": "192.168.100.2/24",
        "status": "active",
        "description": "Example IP 2"
    }
])
```

#### bulk_update_objects

Update multiple objects in NetBox in a single API call.

Arguments:

- `object_type`: String representing the NetBox object type (e.g. "devices", "ip-addresses")
- `data_list`: List of dictionaries, each containing the ID and properties to update

Note: Each object dictionary in the data_list MUST contain an 'id' field.

Example - Updating multiple devices:

```python
bulk_update_objects("devices", [
    {
        "id": 1,
        "status": "planned"
    },
    {
        "id": 2,
        "status": "active"
    }
])
```

#### bulk_delete_objects

Delete multiple objects from NetBox in a single API call.

Arguments:

- `object_type`: String representing the NetBox object type (e.g. "devices", "ip-addresses")
- `id_list`: List of IDs of objects to delete

Example - Deleting multiple IP addresses:

```python
bulk_delete_objects("ip-addresses", [1, 2, 3])
```

### Security and Best Practices

When using write operations, keep these security considerations in mind:

1. **Access Control**: Ensure that the NetBox API token used has appropriate permissions for the operations being performed.

2. **Data Validation**: Always validate input data before sending it to the API to prevent errors or unintended changes.

3. **Audit Trail**: NetBox maintains a change log for object modifications, but consider implementing additional logging in your application.

4. **Concurrency Control**: Be aware that concurrent modifications to the same object might lead to data inconsistency.

5. **Error Handling**: Always handle errors gracefully and provide meaningful error messages to users.

6. **Bulk Operations**: Use bulk operations for better performance when working with multiple objects, but be cautious about the size of the batch to avoid timeouts.

7. **Testing**: Test write operations in a non-production environment before using them in production.