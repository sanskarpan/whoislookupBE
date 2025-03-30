import httpx
from datetime import datetime
from typing import Dict, Any, Union, Optional
from dateutil import parser

from app.config import settings
from app.models.domain_info import DomainInformation
from app.models.contact_info import ContactInformation


class WhoisService:
    """Service for interacting with the Whois API."""
    
    def __init__(self):
        """Initialize the service with API URL and key from settings."""
        self.api_url = settings.WHOIS_API_URL
        self.api_key = settings.API_KEY
    
    async def fetch_domain_data(self, domain_name: str) -> Dict[str, Any]:
        """
        Fetch domain data from the Whois API.
        
        Args:
            domain_name: The domain name to look up
            
        Returns:
            Dict containing the API response
            
        Raises:
            HTTPException: If the API request fails
        """
        try:
            params = {
                "apiKey": self.api_key,
                "domainName": domain_name,
                "outputFormat": "JSON",
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(self.api_url, params=params)
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            # Log the error
            print(f"Error fetching Whois data: {str(e)}")
            raise Exception(f"Failed to fetch domain information: {str(e)}")
    
    def parse_domain_information(self, data: Dict[str, Any]) -> DomainInformation:
        """
        Parse domain information from the Whois API response.
        
        Args:
            data: The API response data
            
        Returns:
            DomainInformation object
        """
        whois_record = data.get("WhoisRecord", {})
        
        # Extract domain name
        domain_name = whois_record.get("domainName", "")
        
        # Extract registrar
        registrar_data = whois_record.get("registrarName", "")
        if not registrar_data and "registrar" in whois_record:
            registrar_data = whois_record.get("registrar", {}).get("name", "")
        
        # Extract dates
        registration_date = self._parse_date(whois_record, "createdDate")
        expiration_date = self._parse_date(whois_record, "expiresDate")
        
        # Calculate estimated domain age
        estimated_domain_age = None
        if registration_date:
            today = datetime.now()
            # Ensure today is also timezone-naive for consistency
            if today.tzinfo is not None:
                today = today.replace(tzinfo=None)
            delta = today - registration_date
            estimated_domain_age = delta.days // 365
        
        # Extract hostnames
        hostnames = self._extract_hostnames(whois_record)
        
        return DomainInformation(
            domain_name=domain_name,
            registrar=registrar_data,
            registration_date=registration_date,
            expiration_date=expiration_date,
            estimated_domain_age=estimated_domain_age,
            hostnames=hostnames,
        )
    
    def parse_contact_information(self, data: Dict[str, Any]) -> ContactInformation:
        """
        Parse contact information from the Whois API response.
        
        Args:
            data: The API response data
            
        Returns:
            ContactInformation object
        """
        whois_record = data.get("WhoisRecord", {})
        contact_info = ContactInformation()
        
        # Get contacts section
        contacts = whois_record.get("registryData", {}).get("contactEmail", "")
        if not contacts:
            contacts = whois_record.get("contactEmail", "")
        
        # Try different possible paths for contact information
        registry_data = whois_record.get("registryData", {})
        domain_data = whois_record
        
        # Extract registrant name
        registrant = self._get_contact_info(domain_data, registry_data, "registrant")
        contact_info.registrant_name = registrant.get("name", "")
        
        # Extract technical contact name
        technical = self._get_contact_info(domain_data, registry_data, "technical")
        contact_info.technical_contact_name = technical.get("name", "")
        
        # Extract administrative contact name
        admin = self._get_contact_info(domain_data, registry_data, "administrative")
        contact_info.administrative_contact_name = admin.get("name", "")
        
        # Extract contact email
        contact_info.contact_email = contacts
        
        return contact_info
    
    def _get_contact_info(
        self, domain_data: Dict[str, Any], registry_data: Dict[str, Any], contact_type: str
    ) -> Dict[str, Any]:
        """
        Extract contact information from whois data.
        
        Args:
            domain_data: The domain data
            registry_data: The registry data
            contact_type: The type of contact to extract (registrant, technical, administrative)
            
        Returns:
            Dict containing the contact information
        """
        # Try to get from registry data first
        contact = registry_data.get(f"{contact_type}Contact", {})
        
        # If not found, try domain data
        if not contact:
            contact = domain_data.get(f"{contact_type}Contact", {})
        
        # If still not found, try other possible structures
        if not contact:
            contact = domain_data.get("registrant", {})
        
        return contact
    
    def _parse_date(self, data: Dict[str, Any], key: str) -> Optional[datetime]:
        """
        Parse a date from the API response.
        
        Args:
            data: The API response data
            key: The key of the date field
            
        Returns:
            Parsed datetime object or None
        """
        date_str = data.get(key)
        
        # If date not found in top level, check registryData
        if not date_str and "registryData" in data:
            date_str = data.get("registryData", {}).get(key)
        
        # If still not found, try other structures
        if not date_str:
            date_str = data.get("registryData", {}).get("registry", {}).get(key)
        
        try:
            if date_str:
                # Parse the date and make it timezone-naive to prevent timezone comparison issues
                dt = parser.parse(date_str)
                if dt.tzinfo is not None:
                    # Convert to naive datetime by replacing tzinfo
                    dt = dt.replace(tzinfo=None)
                return dt
            return None
        except (ValueError, TypeError):
            return None
    
    def _extract_hostnames(self, data: Dict[str, Any]) -> str:
        """
        Extract and format hostnames from the API response.
        
        Args:
            data: The API response data
            
        Returns:
            Formatted hostname string
        """
        hostnames = []
        
        # Try to get nameServers from various possible locations
        name_servers = data.get("nameServers", [])
        
        if isinstance(name_servers, list):
            for server in name_servers:
                if isinstance(server, dict) and "hostName" in server:
                    hostnames.append(server["hostName"])
                elif isinstance(server, str):
                    hostnames.append(server)
        
        # If not found, try registryData
        if not hostnames and "registryData" in data:
            registry_data = data.get("registryData", {})
            name_servers = registry_data.get("nameServers", [])
            
            if isinstance(name_servers, list):
                for server in name_servers:
                    if isinstance(server, dict) and "hostName" in server:
                        hostnames.append(server["hostName"])
                    elif isinstance(server, str):
                        hostnames.append(server)
        
        # Join hostnames and truncate if too long
        if hostnames:
            hostname_str = ", ".join(hostnames)
            if len(hostname_str) > 25:
                return hostname_str[:22] + "..."
            return hostname_str
        
        return ""