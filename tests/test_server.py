import pytest
from unittest.mock import patch, MagicMock
import json
from .mocks.netbox_responses import (
    get_devices_response,
    get_ip_addresses_response,
    get_sites_response,
    API_ERROR_RESPONSES
)

def test_get_objects_tool(mock_mcp_server, mock_netbox_client):
    """Test the get_objects MCP tool"""
    with patch('server.netbox', mock_netbox_client):
        # Test getting devices
        result = mock_mcp_server._tools['get_objects'](
            object_type="devices",
            filters={"name": "test-device"}
        )
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "test-device-01"

        # Test getting IP addresses
        result = mock_mcp_server._tools['get_objects'](
            object_type="ip-addresses",
            filters={"address": "192.168.1.1"}
        )
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["address"] == "192.168.1.1/24"

        # Test getting sites
        result = mock_mcp_server._tools['get_objects'](
            object_type="sites",
            filters={"name": "Main"}
        )
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "Main Site"

def test_get_objects_invalid_type(mock_mcp_server, mock_netbox_client):
    """Test get_objects tool with invalid object type"""
    with patch('server.netbox', mock_netbox_client):
        with pytest.raises(ValueError) as exc_info:
            mock_mcp_server._tools['get_objects'](
                object_type="invalid-type",
                filters={}
            )
        assert "Invalid object_type" in str(exc_info.value)

def test_search_netbox_tool(mock_mcp_server, mock_netbox_client):
    """Test the search_netbox MCP tool"""
    with patch('server.netbox', mock_netbox_client):
        # Test basic search
        result = mock_mcp_server._tools['search_netbox'](
            query="test-device",
            limit=10
        )
        assert isinstance(result, list)
        
        # Test search with custom limit
        result = mock_mcp_server._tools['search_netbox'](
            query="test-device",
            limit=5
        )
        assert isinstance(result, list)

def test_get_object_by_id_tool(mock_mcp_server, mock_netbox_client, sample_device_response):
    """Test the get_object_by_id MCP tool"""
    with patch('server.netbox', mock_netbox_client):
        # Test getting device by ID
        result = mock_mcp_server._tools['get_object_by_id'](
            object_type="devices",
            object_id=123
        )
        assert isinstance(result, dict)
        assert result["id"] == 123
        assert result["name"] == "test-device-01"

        # Test invalid object type
        with pytest.raises(ValueError) as exc_info:
            mock_mcp_server._tools['get_object_by_id'](
                object_type="invalid-type",
                object_id=123
            )
        assert "Invalid object_type" in str(exc_info.value)

def test_error_handling(mock_mcp_server, mock_netbox_client, mock_responses):
    """Test error handling in MCP tools"""
    with patch('server.netbox', mock_netbox_client):
        # Test 404 Not Found
        with pytest.raises(Exception) as exc_info:
            mock_mcp_server._tools['get_object_by_id'](
                object_type="devices",
                object_id=999
            )
        assert "Not found" in str(exc_info.value)

        # Test authentication error
        with pytest.raises(Exception) as exc_info:
            mock_mcp_server._tools['get_objects'](
                object_type="devices",
                filters={"token": "invalid"}
            )
        assert "Invalid token" in str(exc_info.value)

def test_tool_registration(mock_mcp_server):
    """Test that all required tools are registered"""
    expected_tools = {
        'get_objects',
        'search_netbox',
        'get_object_by_id'
    }
    
    registered_tools = set(mock_mcp_server._tools.keys())
    assert expected_tools.issubset(registered_tools), \
        f"Missing tools: {expected_tools - registered_tools}"

def test_tool_parameter_validation(mock_mcp_server, mock_netbox_client):
    """Test parameter validation in MCP tools"""
    with patch('server.netbox', mock_netbox_client):
        # Test missing required parameters
        with pytest.raises(TypeError):
            mock_mcp_server._tools['get_objects'](filters={})
            
        with pytest.raises(TypeError):
            mock_mcp_server._tools['get_object_by_id'](object_type="devices")
            
        # Test invalid parameter types
        with pytest.raises(TypeError):
            mock_mcp_server._tools['get_objects'](
                object_type=123,  # Should be string
                filters={}
            )
            
        with pytest.raises(TypeError):
            mock_mcp_server._tools['get_object_by_id'](
                object_type="devices",
                object_id="123"  # Should be integer
            )

def test_response_format(mock_mcp_server, mock_netbox_client):
    """Test that responses follow the expected format"""
    with patch('server.netbox', mock_netbox_client):
        # Test list response format
        result = mock_mcp_server._tools['get_objects'](
            object_type="devices",
            filters={}
        )
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, dict)
            assert "id" in item
            assert "name" in item
        
        # Test single object response format
        result = mock_mcp_server._tools['get_object_by_id'](
            object_type="devices",
            object_id=123
        )
        assert isinstance(result, dict)
        assert "id" in result
        assert "name" in result
        assert "url" in result
