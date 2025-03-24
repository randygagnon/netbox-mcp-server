import pytest
from unittest.mock import patch
import responses
from .mocks.netbox_responses import (
    get_devices_response,
    get_ip_addresses_response,
    get_sites_response,
    API_ERROR_RESPONSES
)

def test_full_device_workflow(mock_mcp_server, mock_netbox_client, mock_responses, sample_device_response):
    """Test a complete device management workflow"""
    with patch('server.netbox', mock_netbox_client):
        # 1. Search for devices
        search_result = mock_mcp_server._tools['search_netbox'](
            query="test-device",
            limit=10
        )
        assert isinstance(search_result, list)
        
        # 2. Get specific device details
        device = mock_mcp_server._tools['get_object_by_id'](
            object_type="devices",
            object_id=123
        )
        assert device["name"] == "test-device-01"
        
        # 3. Get device interfaces
        interfaces = mock_mcp_server._tools['get_objects'](
            object_type="interfaces",
            filters={"device_id": 123}
        )
        assert isinstance(interfaces, list)
        
        # 4. Get IP addresses for device
        ip_addresses = mock_mcp_server._tools['get_objects'](
            object_type="ip-addresses",
            filters={"device_id": 123}
        )
        assert isinstance(ip_addresses, list)

def test_site_and_rack_workflow(mock_mcp_server, mock_netbox_client, mock_responses):
    """Test site and rack management workflow"""
    with patch('server.netbox', mock_netbox_client):
        # 1. Get all sites
        sites = mock_mcp_server._tools['get_objects'](
            object_type="sites",
            filters={}
        )
        assert isinstance(sites, list)
        assert len(sites) > 0
        
        # 2. Get specific site
        site = mock_mcp_server._tools['get_object_by_id'](
            object_type="sites",
            object_id=1
        )
        assert site["name"] == "Main Site"
        
        # 3. Get racks in site
        racks = mock_mcp_server._tools['get_objects'](
            object_type="racks",
            filters={"site_id": 1}
        )
        assert isinstance(racks, list)

def test_ip_management_workflow(mock_mcp_server, mock_netbox_client, mock_responses):
    """Test IP address management workflow"""
    with patch('server.netbox', mock_netbox_client):
        # 1. Get all IP addresses
        ips = mock_mcp_server._tools['get_objects'](
            object_type="ip-addresses",
            filters={}
        )
        assert isinstance(ips, list)
        
        # 2. Get specific IP
        ip = mock_mcp_server._tools['get_object_by_id'](
            object_type="ip-addresses",
            object_id=456
        )
        assert ip["address"] == "192.168.1.1/24"
        
        # 3. Get related prefix
        prefixes = mock_mcp_server._tools['get_objects'](
            object_type="prefixes",
            filters={"contains": "192.168.1.1"}
        )
        assert isinstance(prefixes, list)

def test_error_recovery_workflow(mock_mcp_server, mock_netbox_client, mock_responses):
    """Test error handling and recovery in a workflow"""
    with patch('server.netbox', mock_netbox_client):
        # 1. Try to get non-existent device
        with pytest.raises(Exception):
            mock_mcp_server._tools['get_object_by_id'](
                object_type="devices",
                object_id=999
            )
        
        # 2. Recover by searching
        search_result = mock_mcp_server._tools['search_netbox'](
            query="test-device",
            limit=10
        )
        assert isinstance(search_result, list)
        
        # 3. Get valid device
        device = mock_mcp_server._tools['get_object_by_id'](
            object_type="devices",
            object_id=123
        )
        assert device["name"] == "test-device-01"

def test_concurrent_operations(mock_mcp_server, mock_netbox_client, mock_responses):
    """Test multiple operations happening in sequence"""
    with patch('server.netbox', mock_netbox_client):
        # 1. Get devices and sites simultaneously
        devices = mock_mcp_server._tools['get_objects'](
            object_type="devices",
            filters={}
        )
        sites = mock_mcp_server._tools['get_objects'](
            object_type="sites",
            filters={}
        )
        assert isinstance(devices, list)
        assert isinstance(sites, list)
        
        # 2. Get specific device and its IPs
        device = mock_mcp_server._tools['get_object_by_id'](
            object_type="devices",
            object_id=123
        )
        ips = mock_mcp_server._tools['get_objects'](
            object_type="ip-addresses",
            filters={"device_id": 123}
        )
        assert device["name"] == "test-device-01"
        assert isinstance(ips, list)

def test_search_and_filter_workflow(mock_mcp_server, mock_netbox_client, mock_responses):
    """Test search and filter combinations"""
    with patch('server.netbox', mock_netbox_client):
        # 1. Search for devices
        search_result = mock_mcp_server._tools['search_netbox'](
            query="test",
            limit=10
        )
        assert isinstance(search_result, list)
        
        # 2. Filter devices by site
        devices = mock_mcp_server._tools['get_objects'](
            object_type="devices",
            filters={"site": "Main Site"}
        )
        assert isinstance(devices, list)
        
        # 3. Get IPs for filtered devices
        for device in devices:
            ips = mock_mcp_server._tools['get_objects'](
                object_type="ip-addresses",
                filters={"device_id": device["id"]}
            )
            assert isinstance(ips, list)
