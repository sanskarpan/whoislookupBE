from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DomainInformation(BaseModel):
    """Model for domain information returned from Whois API."""
    
    domain_name: str
    registrar: Optional[str] = None
    registration_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    estimated_domain_age: Optional[int] = None
    hostnames: Optional[str] = None
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "domain_name": "amazon.com",
                "registrar": "Amazon Registrar, Inc.",
                "registration_date": "1995-05-12",
                "expiration_date": "2026-05-12",
                "estimated_domain_age": 29,
                "hostnames": "ns1.amazon.com, ns2.amazon..."
            }
        }


class DomainRequest(BaseModel):
    """Model for domain search request."""
    
    domain_name: str = Field(..., description="Domain name to search")
    info_type: str = Field(..., description="Type of information to retrieve: domain or contact")
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "domain_name": "amazon.com",
                "info_type": "domain"
            }
        }