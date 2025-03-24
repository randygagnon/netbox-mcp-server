import pytest
import responses
from requests.exceptions import HTTPError
from netbox_client import NetBoxRestClient
from .mocks.netbox_responses import (
    get_devices_response,
    get_ip_addresses_response,
    get_sites_response,
    API_ERROR_RESPONSES
)

def test_client_initialization(mock_netbox_url, mock_netbox_token):
    """Test NetBox client initialization"""
    client = NetBoxRestClient(mock_netbox_url, mock_netbox_token)
    assert client.base_url == mock_netbox_url.rstrip('/')
    assert client.api_url == f"{mock_netbox_url.rstrip('/')}/api"
    assert client.token == mock_netbox_token
    assert client.verify_ssl is True

def test_get_devices(mock_netbox_client, mock_responses):
    """Test getting devices from NetBox"""
    # Setup mock response
    mock_responses.add(
        responses.GET,
        f"{mock_netbox_client.api_url}/dcim/devices/",
        json=get_devices_response(),
        status=200
    )
    
    # Test successful request
    devices = mock_netbox_client.get("dcim/devices")
    assert len(devices) == 1
    assert devices[0]["name"] == "test-device-01"
    assert devices[0]["device_type"]["manufacturer"]["name"] == "Cisco"

def test_get_device_by_id(mock_netbox_client, mock_responses, sample_device_response):
    """Test getting a specific device by ID"""
    device_id = 123
    
    # Setup mock response
    mock_responses.add(
        responses.GET,
        f"{mock_netbox_client.api_url}/dcim/devices/{device_id}/",
        json=sample_device_response,
        status=200
    )
    
    # Test successful request
    device = mock_netbox_client.get("dcim/devices", id=device_id)
    assert device["id"] == device_id
    assert device["name"] == "test-device-01"
    assert device["serial"] == "FTX1234567890"

def test_get_ip_addresses(mock_netbox_client, mock_responses):
    """Test getting IP addresses from NetBox"""
    # Setup mock response
    mock_responses.add(
        responses.GET,
        f"{mock_netbox_client.api_url}/ipam/ip-addresses/",
        json=get_ip_addresses_response(),
        status=200
    )
    
    # Test successful request
    ip_addresses = mock_netbox_client.get("ipam/ip-addresses")
    assert len(ip_addresses) == 1
    assert ip_addresses[0]["address"] == "192.168.1.1/24"
    assert ip_addresses[0]["assigned_object"]["device"]["name"] == "test-device-01"

def test_get_sites(mock_netbox_client, mock_responses):
    """Test getting sites from NetBox"""
    # Setup mock response
    mock_responses.add(
        responses.GET,
        f"{mock_netbox_client.api_url}/dcim/sites/",
        json=get_sites_response(),
        status=200
    )
    
    # Test successful request
    sites = mock_netbox_client.get("dcim/sites")
    assert len(sites) == 1
    assert sites[0]["name"] == "Main Site"
    assert sites[0]["slug"] == "main-site"

def test_create_device(mock_netbox_client, mock_responses, sample_device_response):
    """Test creating a new device"""
    new_device_data = {
        "name": "test-device-01",
        "device_type": 1,
        "device_role": 1,
        "site": 1
    }
    
    # Setup mock response
    mock_responses.add(
        responses.POST,
        f"{mock_netbox_client.api_url}/dcim/devices/",
        json=sample_device_response,
        status=201
    )
    
    # Test successful creation
    created_device = mock_netbox_client.create("dcim/devices", new_device_data)
    assert created_device["name"] == "test-device-01"
    assert created_device["id"] == 123

def test_update_device(mock_netbox_client, mock_responses, sample_device_response):
    """Test updating an existing device"""
    device_id = 123
    update_data = {
        "name": "updated-device-01"
    }
    
    updated_response = sample_device_response.copy()
    updated_response["name"] = "updated-device-01"
    
    # Setup mock response
    mock_responses.add(
        responses.PATCH,
        f"{mock_netbox_client.api_url}/dcim/devices/{device_id}/",
        json=updated_response,
        status=200
    )
    
    # Test successful update
    updated_device = mock_netbox_client.update("dcim/devices", device_id, update_data)
    assert updated_device["name"] == "updated-device-01"
    assert updated_device["id"] == device_id

def test_delete_device(mock_netbox_client, mock_responses):
    """Test deleting a device"""
    device_id = 123
    
    # Setup mock response
    mock_responses.add(
        responses.DELETE,
        f"{mock_netbox_client.api_url}/dcim/devices/{device_id}/",
        status=204
    )
    
    # Test successful deletion
    assert mock_netbox_client.delete("dcim/devices", device_id) is True

def test_error_handling(mock_netbox_client, mock_responses):
    """Test error handling for various HTTP errors"""
    # Test 404 Not Found
    mock_responses.add(
        responses.GET,
        f"{mock_netbox_client.api_url}/dcim/devices/999/",
        json=API_ERROR_RESPONSES["not_found"],
        status=404
    )
    
    with pytest.raises(HTTPError) as exc_info:
        mock_netbox_client.get("dcim/devices", id=999)
    assert exc_info.value.response.status_code == 404
    
    # Test 401 Unauthorized
    mock_responses.add(
        responses.GET,
        f"{mock_netbox_client.api_url}/dcim/devices/",
        json=API_ERROR_RESPONSES["authentication_error"],
        status=401
    )
    
    with pytest.raises(HTTPError) as exc_info:
        mock_netbox_client.get("dcim/devices")
    assert exc_info.value.response.status_code == 401
    
    # Test 403 Forbidden
    mock_responses.add(
        responses.POST,
        f"{mock_netbox_client.api_url}/dcim/devices/",
        json=API_ERROR_RESPONSES["permission_error"],
        status=403
    )
    
    with pytest.raises(HTTPError) as exc_info:
        mock_netbox_client.create("dcim/devices", {"name": "test"})
    assert exc_info.value.response.status_code == 403
