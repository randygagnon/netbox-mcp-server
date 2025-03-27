#!/usr/bin/env python3
"""
NetBox Client Library

This module provides a base class for NetBox client implementations and a REST API implementation.
"""

import abc
from typing import Any, Dict, List, Optional, Union
import requests


class NetBoxClientBase(abc.ABC):
    """
    Abstract base class for NetBox client implementations.
    
    This class defines the interface for CRUD operations that can be implemented
    either via the REST API or directly via the ORM in a NetBox plugin.
    """
    
    @abc.abstractmethod
    def get(self, endpoint: str, id: Optional[int] = None, params: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Retrieve one or more objects from NetBox.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            id: Optional ID to retrieve a specific object
            params: Optional query parameters for filtering
            
        Returns:
            Either a single object dict or a list of object dicts
        """
        pass
    
    @abc.abstractmethod
    def create(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new object in NetBox.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            data: Object data to create
            
        Returns:
            The created object as a dict
        """
        pass
    
    @abc.abstractmethod
    def update(self, endpoint: str, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing object in NetBox.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            id: ID of the object to update
            data: Object data to update
            
        Returns:
            The updated object as a dict
        """
        pass
    
    @abc.abstractmethod
    def delete(self, endpoint: str, id: int) -> bool:
        """
        Delete an object from NetBox.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            id: ID of the object to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abc.abstractmethod
    def bulk_create(self, endpoint: str, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create multiple objects in NetBox.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            data: List of object data to create
            
        Returns:
            List of created objects as dicts
        """
        pass
    
    @abc.abstractmethod
    def bulk_update(self, endpoint: str, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Update multiple objects in NetBox.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            data: List of object data to update (must include ID)
            
        Returns:
            List of updated objects as dicts
        """
        pass
    
    @abc.abstractmethod
    def bulk_delete(self, endpoint: str, ids: List[int]) -> bool:
        """
        Delete multiple objects from NetBox.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            ids: List of IDs to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass


class NetBoxRestClient(NetBoxClientBase):
    """
    NetBox client implementation using the REST API.
    """

# # Example of how to use the client
# client = NetBoxRestClient(
#     url="https://netbox.example.com",
#     token="your_api_token_here",
#     verify_ssl=True
# )
    
# # Get all sites
# sites = client.get("dcim/sites")
# print(f"Found {len(sites)} sites")
    
# # Get a specific site
# site = client.get("dcim/sites", id=1)
# print(f"Site name: {site.get('name')}")
    
# # Create a new site
# new_site = client.create("dcim/sites", {
#     "name": "New Site",
#     "slug": "new-site",
#     "status": "active"
# })
# print(f"Created site: {new_site.get('name')} (ID: {new_site.get('id')})")

    def __init__(self, url: str, token: str, verify_ssl: bool = True, branch: Optional[str] = None):
        """
        Initialize the REST API client.
        
        Args:
            url: The base URL of the NetBox instance (e.g., 'https://netbox.example.com')
            token: API token for authentication
            verify_ssl: Whether to verify SSL certificates
            branch: Optional schema ID of the branch to use for all operations
        """
        self.base_url = url.rstrip('/')
        self.api_url = f"{self.base_url}/api"
        self.token = token
        self.verify_ssl = verify_ssl
        self.branch = branch
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        
        # Add branch header if specified
        if self.branch:
            self.session.headers.update({
                'X-NetBox-Branch': self.branch
            })
    
    def set_branch(self, branch: str) -> None:
        """
        Set or change the active branch for subsequent API calls.
        
        Args:
            branch: Schema ID of the branch to use
        """
        self.branch = branch
        if branch:
            self.session.headers.update({
                'X-NetBox-Branch': branch
            })
        elif 'X-NetBox-Branch' in self.session.headers:
            # Remove branch header if branch is None
            del self.session.headers['X-NetBox-Branch']
    
    def clear_branch(self) -> None:
        """Remove the active branch (use the main/default branch)."""
        self.set_branch(None)
    
    def _build_url(self, endpoint: str, id: Optional[int] = None) -> str:
        """Build the full URL for an API request."""
        endpoint = endpoint.strip('/')
        if id is not None:
            return f"{self.api_url}/{endpoint}/{id}/"
        return f"{self.api_url}/{endpoint}/"
    
    def get(self, endpoint: str, id: Optional[int] = None, params: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Retrieve one or more objects from NetBox via the REST API.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            id: Optional ID to retrieve a specific object
            params: Optional query parameters for filtering
            
        Returns:
            Either a single object dict or a list of object dicts
        
        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._build_url(endpoint, id)
        response = self.session.get(url, params=params, verify=self.verify_ssl)
        response.raise_for_status()
        
        data = response.json()
        if id is None and 'results' in data:
            # Handle paginated results
            return data['results']
        return data
    
    def create(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new object in NetBox via the REST API.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            data: Object data to create
            
        Returns:
            The created object as a dict
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._build_url(endpoint)
        response = self.session.post(url, json=data, verify=self.verify_ssl)
        response.raise_for_status()
        return response.json()
    
    def update(self, endpoint: str, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing object in NetBox via the REST API.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            id: ID of the object to update
            data: Object data to update
            
        Returns:
            The updated object as a dict
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._build_url(endpoint, id)
        response = self.session.patch(url, json=data, verify=self.verify_ssl)
        response.raise_for_status()
        return response.json()
    
    def delete(self, endpoint: str, id: int) -> bool:
        """
        Delete an object from NetBox via the REST API.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            id: ID of the object to delete
            
        Returns:
            True if deletion was successful, False otherwise
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._build_url(endpoint, id)
        response = self.session.delete(url, verify=self.verify_ssl)
        response.raise_for_status()
        return response.status_code == 204
    
    def bulk_create(self, endpoint: str, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create multiple objects in NetBox via the REST API.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            data: List of object data to create
            
        Returns:
            List of created objects as dicts
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = f"{self._build_url(endpoint)}bulk/"
        response = self.session.post(url, json=data, verify=self.verify_ssl)
        response.raise_for_status()
        return response.json()
    
    def bulk_update(self, endpoint: str, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Update multiple objects in NetBox via the REST API.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            data: List of object data to update (must include ID)
            
        Returns:
            List of updated objects as dicts
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = f"{self._build_url(endpoint)}bulk/"
        response = self.session.patch(url, json=data, verify=self.verify_ssl)
        response.raise_for_status()
        return response.json()
    
    def bulk_delete(self, endpoint: str, ids: List[int]) -> bool:
        """
        Delete multiple objects from NetBox via the REST API.
        
        Args:
            endpoint: The API endpoint (e.g., 'dcim/sites', 'ipam/prefixes')
            ids: List of IDs to delete
            
        Returns:
            True if deletion was successful, False otherwise
        
        Raises:
            requests.HTTPError: If the request fails
        """
        url = f"{self._build_url(endpoint)}bulk/delete/"
        data = {"id": ids}
        response = self.session.post(url, json=data, verify=self.verify_ssl)
        response.raise_for_status()
        return True
    
    # Branch-specific methods
    
    def get_branches(self) -> List[Dict[str, Any]]:
        """
        Retrieve all branches from NetBox.
        
        Returns:
            List of branch objects
        
        Raises:
            requests.HTTPError: If the request fails
        """
        return self.get("extras/branches")
    
    def get_branch(self, id: int) -> Dict[str, Any]:
        """
        Retrieve a specific branch by ID.
        
        Args:
            id: Branch ID
            
        Returns:
            Branch object
            
        Raises:
            requests.HTTPError: If the request fails
        """
        return self.get("extras/branches", id=id)
    
    def create_branch(self, name: str, description: str = "", base_branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new branch in NetBox.
        
        Args:
            name: Name of the branch
            description: Optional description
            base_branch: Optional schema ID of a branch to base this one on
            
        Returns:
            The created branch object
            
        Raises:
            requests.HTTPError: If the request fails
        """
        data = {
            "name": name,
            "description": description,
        }
        
        # If base_branch is specified, include it
        if base_branch:
            data["base_branch"] = base_branch
            
        # X-NetBox-Branch header is NOT used when creating a branch
        # Temporarily clear the header if it's set
        current_branch = self.branch
        if current_branch:
            self.clear_branch()
            
        try:
            result = self.create("extras/branches", data)
            return result
        finally:
            # Restore the branch if it was set
            if current_branch:
                self.set_branch(current_branch)
    
    def update_branch(self, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a branch in NetBox.
        
        Args:
            id: Branch ID
            data: Branch data to update
            
        Returns:
            The updated branch object
            
        Raises:
            requests.HTTPError: If the request fails
        """
        # X-NetBox-Branch header is NOT used when updating a branch
        # Temporarily clear the header if it's set
        current_branch = self.branch
        if current_branch:
            self.clear_branch()
            
        try:
            result = self.update("extras/branches", id, data)
            return result
        finally:
            # Restore the branch if it was set
            if current_branch:
                self.set_branch(current_branch)
    
    def delete_branch(self, id: int) -> bool:
        """
        Delete a branch from NetBox.
        
        Args:
            id: Branch ID
            
        Returns:
            True if deletion was successful
            
        Raises:
            requests.HTTPError: If the request fails
        """
        # X-NetBox-Branch header is NOT used when deleting a branch
        # Temporarily clear the header if it's set
        current_branch = self.branch
        if current_branch:
            self.clear_branch()
            
        try:
            result = self.delete("extras/branches", id)
            return result
        finally:
            # Restore the branch if it was set
            if current_branch:
                self.set_branch(current_branch)
    
    def merge_branch(self, id: int, target_branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Merge a branch into either the main branch or another branch.
        
        Args:
            id: ID of the branch to merge
            target_branch: Optional schema ID of the target branch (defaults to main branch)
            
        Returns:
            Result of the merge operation
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._build_url(f"extras/branches/{id}/merge")
        data = {}
        if target_branch:
            data["target_branch"] = target_branch
        
        # X-NetBox-Branch header is NOT used when merging a branch
        # Temporarily clear the header if it's set
        current_branch = self.branch
        if current_branch:
            self.clear_branch()
            
        try:
            response = self.session.post(url, json=data, verify=self.verify_ssl)
            response.raise_for_status()
            return response.json()
        finally:
            # Restore the branch if it was set
            if current_branch:
                self.set_branch(current_branch)
