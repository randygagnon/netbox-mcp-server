"""
Mock responses for NetBox API endpoints based on real NetBox API structure
"""

def get_paginated_response(results, count=None):
    """Helper to create paginated response format"""
    if count is None:
        count = len(results)
    return {
        "count": count,
        "next": None,
        "previous": None,
        "results": results
    }

def get_devices_response(devices=None):
    """Mock response for /api/dcim/devices/ endpoint"""
    if devices is None:
        devices = [{
            "id": 123,
            "name": "test-device-01",
            "device_type": {
                "id": 1,
                "manufacturer": {"name": "Cisco"},
                "model": "ISR4321"
            },
            "status": {"value": "active", "label": "Active"},
            "site": {"name": "Main Site"}
        }]
    return get_paginated_response(devices)

def get_ip_addresses_response(ip_addresses=None):
    """Mock response for /api/ipam/ip-addresses/ endpoint"""
    if ip_addresses is None:
        ip_addresses = [{
            "id": 456,
            "address": "192.168.1.1/24",
            "status": {"value": "active", "label": "Active"},
            "assigned_object_type": "dcim.interface",
            "assigned_object": {
                "device": {"name": "test-device-01"},
                "name": "GigabitEthernet0/0/1"
            }
        }]
    return get_paginated_response(ip_addresses)

def get_sites_response(sites=None):
    """Mock response for /api/dcim/sites/ endpoint"""
    if sites is None:
        sites = [{
            "id": 1,
            "name": "Main Site",
            "slug": "main-site",
            "status": {"value": "active", "label": "Active"}
        }]
    return get_paginated_response(sites)

def get_interfaces_response(interfaces=None):
    """Mock response for /api/dcim/interfaces/ endpoint"""
    if interfaces is None:
        interfaces = [{
            "id": 789,
            "name": "GigabitEthernet0/0/1",
            "type": {"value": "1000base-t", "label": "1000BASE-T"},
            "device": {"id": 123, "name": "test-device-01"},
            "enabled": True,
            "mac_address": "00:11:22:33:44:55"
        }]
    return get_paginated_response(interfaces)

def get_vlans_response(vlans=None):
    """Mock response for /api/ipam/vlans/ endpoint"""
    if vlans is None:
        vlans = [{
            "id": 101,
            "vid": 100,
            "name": "Management",
            "status": {"value": "active", "label": "Active"}
        }]
    return get_paginated_response(vlans)

def get_prefixes_response(prefixes=None):
    """Mock response for /api/ipam/prefixes/ endpoint"""
    if prefixes is None:
        prefixes = [{
            "id": 201,
            "prefix": "192.168.1.0/24",
            "status": {"value": "active", "label": "Active"},
            "vrf": None
        }]
    return get_paginated_response(prefixes)

# Error responses
API_ERROR_RESPONSES = {
    "not_found": {
        "detail": "Not found."
    },
    "validation_error": {
        "name": ["This field is required."]
    },
    "authentication_error": {
        "detail": "Invalid token."
    },
    "permission_error": {
        "detail": "You do not have permission to perform this action."
    }
}
