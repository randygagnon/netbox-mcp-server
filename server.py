from mcp.server.fastmcp import FastMCP
from netbox_client import NetBoxRestClient
import os
import requests
import json

# Mapping of simple object names to API endpoints
NETBOX_OBJECT_TYPES = {
    # DCIM (Device and Infrastructure)
    "cables": "dcim/cables",
    "console-ports": "dcim/console-ports", 
    "console-server-ports": "dcim/console-server-ports",
    "devices": "dcim/devices",
    "device-bays": "dcim/device-bays",
    "device-roles": "dcim/device-roles",
    "device-types": "dcim/device-types",
    "front-ports": "dcim/front-ports",
    "interfaces": "dcim/interfaces",
    "inventory-items": "dcim/inventory-items",
    "locations": "dcim/locations",
    "manufacturers": "dcim/manufacturers",
    "modules": "dcim/modules",
    "module-bays": "dcim/module-bays",
    "module-types": "dcim/module-types",
    "platforms": "dcim/platforms",
    "power-feeds": "dcim/power-feeds",
    "power-outlets": "dcim/power-outlets",
    "power-panels": "dcim/power-panels",
    "power-ports": "dcim/power-ports",
    "racks": "dcim/racks",
    "rack-reservations": "dcim/rack-reservations",
    "rack-roles": "dcim/rack-roles",
    "regions": "dcim/regions",
    "sites": "dcim/sites",
    "site-groups": "dcim/site-groups",
    "virtual-chassis": "dcim/virtual-chassis",
    
    # IPAM (IP Address Management)
    "asns": "ipam/asns",
    "asn-ranges": "ipam/asn-ranges", 
    "aggregates": "ipam/aggregates",
    "fhrp-groups": "ipam/fhrp-groups",
    "ip-addresses": "ipam/ip-addresses",
    "ip-ranges": "ipam/ip-ranges",
    "prefixes": "ipam/prefixes",
    "rirs": "ipam/rirs",
    "roles": "ipam/roles",
    "route-targets": "ipam/route-targets",
    "services": "ipam/services",
    "vlans": "ipam/vlans",
    "vlan-groups": "ipam/vlan-groups",
    "vrfs": "ipam/vrfs",
    
    # Circuits
    "circuits": "circuits/circuits",
    "circuit-types": "circuits/circuit-types",
    "circuit-terminations": "circuits/circuit-terminations",
    "providers": "circuits/providers",
    "provider-networks": "circuits/provider-networks",
    
    # Virtualization
    "clusters": "virtualization/clusters",
    "cluster-groups": "virtualization/cluster-groups",
    "cluster-types": "virtualization/cluster-types",
    "virtual-machines": "virtualization/virtual-machines",
    "vm-interfaces": "virtualization/interfaces",
    
    # Tenancy
    "tenants": "tenancy/tenants",
    "tenant-groups": "tenancy/tenant-groups",
    "contacts": "tenancy/contacts",
    "contact-groups": "tenancy/contact-groups",
    "contact-roles": "tenancy/contact-roles",
    
    # VPN
    "ike-policies": "vpn/ike-policies",
    "ike-proposals": "vpn/ike-proposals",
    "ipsec-policies": "vpn/ipsec-policies",
    "ipsec-profiles": "vpn/ipsec-profiles",
    "ipsec-proposals": "vpn/ipsec-proposals",
    "l2vpns": "vpn/l2vpns",
    "tunnels": "vpn/tunnels",
    "tunnel-groups": "vpn/tunnel-groups",
    
    # Wireless
    "wireless-lans": "wireless/wireless-lans",
    "wireless-lan-groups": "wireless/wireless-lan-groups",
    "wireless-links": "wireless/wireless-links"
}

mcp = FastMCP("NetBox", log_level="DEBUG")
netbox = None

@mcp.tool()
def get_objects(object_type: str, filters: dict):
    """
    Get objects from NetBox based on their type and filters
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        filters: dict of filters to apply to the API call based on the NetBox API filtering options
    
    Valid object_type values:
    
    DCIM (Device and Infrastructure):
    - cables
    - console-ports
    - console-server-ports  
    - devices
    - device-bays
    - device-roles
    - device-types
    - front-ports
    - interfaces
    - inventory-items
    - locations
    - manufacturers
    - modules
    - module-bays
    - module-types
    - platforms
    - power-feeds
    - power-outlets
    - power-panels
    - power-ports
    - racks
    - rack-reservations
    - rack-roles
    - regions
    - sites
    - site-groups
    - virtual-chassis
    
    IPAM (IP Address Management):
    - asns
    - asn-ranges
    - aggregates 
    - fhrp-groups
    - ip-addresses
    - ip-ranges
    - prefixes
    - rirs
    - roles
    - route-targets
    - services
    - vlans
    - vlan-groups
    - vrfs
    
    Circuits:
    - circuits
    - circuit-types
    - circuit-terminations
    - providers
    - provider-networks
    
    Virtualization:
    - clusters
    - cluster-groups
    - cluster-types
    - virtual-machines
    - vm-interfaces
    
    Tenancy:
    - tenants
    - tenant-groups
    - contacts
    - contact-groups
    - contact-roles
    
    VPN:
    - ike-policies
    - ike-proposals
    - ipsec-policies
    - ipsec-profiles
    - ipsec-proposals
    - l2vpns
    - tunnels
    - tunnel-groups
    
    Wireless:
    - wireless-lans
    - wireless-lan-groups
    - wireless-links
    
    See NetBox API documentation for filtering options for each object type.
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")

    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]

    # Make API call
    return netbox.get(endpoint, params=filters)

@mcp.tool()
def search_netbox(query: str, limit: int = 10):
    """
    Perform a global search across NetBox objects.
    
    Args:
        query: Search string to look for across NetBox objects
        limit: Maximum number of results to return (default: 10)
    
    Returns:
        List of matching objects across different NetBox models
    """
    return netbox.get("search", params={"q": query, "limit": limit})

@mcp.tool()
def get_object_by_id(object_type: str, object_id: int):
    """
    Get detailed information about a specific NetBox object by its ID.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        object_id: The numeric ID of the object
    
    Returns:
        Complete object details
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
    
    # Get API endpoint from mapping
    endpoint = f"{NETBOX_OBJECT_TYPES[object_type]}/{object_id}"
    
    return netbox.get(endpoint)

@mcp.tool()
def create_object(object_type: str, data: dict):
    """
    Create a new object in NetBox.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        data: Dictionary containing the object properties to create
    
    Returns:
        The created object details
    
    Examples:
        Creating a new device:
        ```
        {
            "name": "new-device",
            "device_type": 1,
            "device_role": 1,
            "site": 1,
            "status": "active"
        }
        ```
        
        Creating a new IP address:
        ```
        {
            "address": "192.168.100.1/24",
            "status": "active",
            "description": "Example IP"
        }
        ```
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
    
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
    
    # Create the object
    try:
        return netbox.create(endpoint, data)
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_msg = f"Error: {error_details}"
            except (ValueError, json.JSONDecodeError):
                pass
        raise ValueError(f"Failed to create {object_type}: {error_msg}") from e
    except Exception as e:
        raise ValueError(f"Failed to create {object_type}: {str(e)}") from e

@mcp.tool()
def update_object(object_type: str, object_id: int, data: dict):
    """
    Update an existing object in NetBox.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        object_id: The numeric ID of the object to update
        data: Dictionary containing the object properties to update
    
    Returns:
        The updated object details
    
    Examples:
        Updating a device:
        ```
        {
            "name": "updated-device-name",
            "status": "planned"
        }
        ```
        
        Updating an IP address:
        ```
        {
            "description": "Updated description",
            "status": "reserved"
        }
        ```
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
    
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
    
    # Update the object
    try:
        return netbox.update(endpoint, object_id, data)
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_msg = f"Error: {error_details}"
            except (ValueError, json.JSONDecodeError):
                pass
        raise ValueError(f"Failed to update {object_type} with ID {object_id}: {error_msg}") from e
    except Exception as e:
        raise ValueError(f"Failed to update {object_type} with ID {object_id}: {str(e)}") from e

@mcp.tool()
def delete_object(object_type: str, object_id: int):
    """
    Delete an object from NetBox.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        object_id: The numeric ID of the object to delete
    
    Returns:
        True if deletion was successful, False otherwise
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
    
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
    
    # Delete the object
    try:
        result = netbox.delete(endpoint, object_id)
        return result
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_msg = f"Error: {error_details}"
            except (ValueError, json.JSONDecodeError):
                pass
        raise ValueError(f"Failed to delete {object_type} with ID {object_id}: {error_msg}") from e
    except Exception as e:
        raise ValueError(f"Failed to delete {object_type} with ID {object_id}: {str(e)}") from e

@mcp.tool()
def bulk_create_objects(object_type: str, data_list: list):
    """
    Create multiple objects in NetBox in a single API call.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        data_list: List of dictionaries, each containing the properties for one object to create
    
    Returns:
        List of created objects
    
    Examples:
        Creating multiple IP addresses:
        ```
        [
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
        ]
        ```
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
    
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
    
    # Create the objects
    try:
        return netbox.bulk_create(endpoint, data_list)
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_msg = f"Error: {error_details}"
            except (ValueError, json.JSONDecodeError):
                pass
        raise ValueError(f"Failed to bulk create {object_type} objects: {error_msg}") from e
    except Exception as e:
        raise ValueError(f"Failed to bulk create {object_type} objects: {str(e)}") from e

@mcp.tool()
def bulk_update_objects(object_type: str, data_list: list):
    """
    Update multiple objects in NetBox in a single API call.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        data_list: List of dictionaries, each containing the ID and properties to update
    
    Returns:
        List of updated objects
    
    Note:
        Each object dictionary in the data_list MUST contain an 'id' field.
    
    Examples:
        Updating multiple devices:
        ```
        [
            {
                "id": 1,
                "status": "planned"
            },
            {
                "id": 2,
                "status": "active"
            }
        ]
        ```
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
    
    # Validate each item has an ID
    for i, item in enumerate(data_list):
        if 'id' not in item:
            raise ValueError(f"Item at index {i} is missing required 'id' field")
    
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
    
    # Update the objects
    try:
        return netbox.bulk_update(endpoint, data_list)
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_msg = f"Error: {error_details}"
            except (ValueError, json.JSONDecodeError):
                pass
        raise ValueError(f"Failed to bulk update {object_type} objects: {error_msg}") from e
    except Exception as e:
        raise ValueError(f"Failed to bulk update {object_type} objects: {str(e)}") from e

@mcp.tool()
def bulk_delete_objects(object_type: str, id_list: list):
    """
    Delete multiple objects from NetBox in a single API call.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        id_list: List of IDs of objects to delete
    
    Returns:
        True if deletion was successful, False otherwise
    
    Examples:
        Deleting multiple IP addresses:
        ```
        [1, 2, 3]
        ```
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
    
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
    
    # Delete the objects
    try:
        return netbox.bulk_delete(endpoint, id_list)
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_msg = f"Error: {error_details}"
            except (ValueError, json.JSONDecodeError):
                pass
        raise ValueError(f"Failed to bulk delete {object_type} objects: {error_msg}") from e
    except Exception as e:
        raise ValueError(f"Failed to bulk delete {object_type} objects: {str(e)}") from e

if __name__ == "__main__":
    # Load NetBox configuration from environment variables
    netbox_url = os.getenv("NETBOX_URL")
    netbox_token = os.getenv("NETBOX_TOKEN")
    
    if not netbox_url or not netbox_token:
        raise ValueError("NETBOX_URL and NETBOX_TOKEN environment variables must be set")
    
    # Initialize NetBox client
    netbox = NetBoxRestClient(url=netbox_url, token=netbox_token)
    
    mcp.run(transport="stdio")
