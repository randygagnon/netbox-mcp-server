import pytest
from unittest.mock import MagicMock
import responses
from netbox_client import NetBoxRestClient

@pytest.fixture
def mock_netbox_url():
    return "https://netbox.example.com"

@pytest.fixture
def mock_netbox_token():
    return "dummy_token_12345"

@pytest.fixture
def mock_netbox_client(mock_netbox_url, mock_netbox_token):
    return NetBoxRestClient(
        url=mock_netbox_url,
        token=mock_netbox_token,
        verify_ssl=False
    )

@pytest.fixture
def mock_responses():
    with responses.RequestsMock() as rsps:
        yield rsps

@pytest.fixture
def sample_device_response():
    return {
        "id": 123,
        "url": "https://netbox.example.com/api/dcim/devices/123/",
        "name": "test-device-01",
        "device_type": {
            "id": 1,
            "url": "https://netbox.example.com/api/dcim/device-types/1/",
            "manufacturer": {
                "id": 1,
                "url": "https://netbox.example.com/api/dcim/manufacturers/1/",
                "name": "Cisco",
                "slug": "cisco"
            },
            "model": "ISR4321",
            "slug": "isr4321"
        },
        "device_role": {
            "id": 1,
            "url": "https://netbox.example.com/api/dcim/device-roles/1/",
            "name": "Router",
            "slug": "router"
        },
        "tenant": None,
        "platform": {
            "id": 1,
            "url": "https://netbox.example.com/api/dcim/platforms/1/",
            "name": "Cisco IOS",
            "slug": "cisco-ios"
        },
        "serial": "FTX1234567890",
        "asset_tag": None,
        "site": {
            "id": 1,
            "url": "https://netbox.example.com/api/dcim/sites/1/",
            "name": "Main Site",
            "slug": "main-site"
        },
        "rack": None,
        "position": None,
        "face": None,
        "parent_device": None,
        "status": {
            "value": "active",
            "label": "Active"
        },
        "primary_ip4": None,
        "primary_ip6": None,
        "cluster": None,
        "virtual_chassis": None,
        "vc_position": None,
        "vc_priority": None,
        "comments": "",
        "local_context_data": None,
        "tags": [],
        "custom_fields": {},
        "created": "2023-01-01",
        "last_updated": "2023-01-01T00:00:00.000000Z"
    }

@pytest.fixture
def sample_ip_address_response():
    return {
        "id": 456,
        "url": "https://netbox.example.com/api/ipam/ip-addresses/456/",
        "family": {
            "value": 4,
            "label": "IPv4"
        },
        "address": "192.168.1.1/24",
        "vrf": None,
        "tenant": None,
        "status": {
            "value": "active",
            "label": "Active"
        },
        "role": None,
        "assigned_object_type": "dcim.interface",
        "assigned_object_id": 789,
        "assigned_object": {
            "id": 789,
            "url": "https://netbox.example.com/api/dcim/interfaces/789/",
            "device": {
                "id": 123,
                "url": "https://netbox.example.com/api/dcim/devices/123/",
                "name": "test-device-01"
            },
            "name": "GigabitEthernet0/0/1"
        },
        "nat_inside": None,
        "nat_outside": None,
        "dns_name": "",
        "description": "",
        "tags": [],
        "custom_fields": {},
        "created": "2023-01-01",
        "last_updated": "2023-01-01T00:00:00.000000Z"
    }

@pytest.fixture
def sample_site_response():
    return {
        "id": 1,
        "url": "https://netbox.example.com/api/dcim/sites/1/",
        "name": "Main Site",
        "slug": "main-site",
        "status": {
            "value": "active",
            "label": "Active"
        },
        "region": None,
        "tenant": None,
        "facility": "",
        "asn": None,
        "time_zone": "UTC",
        "description": "",
        "physical_address": "",
        "shipping_address": "",
        "latitude": None,
        "longitude": None,
        "contact_name": "",
        "contact_phone": "",
        "contact_email": "",
        "comments": "",
        "tags": [],
        "custom_fields": {},
        "created": "2023-01-01",
        "last_updated": "2023-01-01T00:00:00.000000Z"
    }

@pytest.fixture
def mock_mcp_server():
    """Mock MCP server instance for testing"""
    from server import mcp
    mcp._tools = {}  # Reset tools
    return mcp
