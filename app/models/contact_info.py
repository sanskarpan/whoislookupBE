from typing import Optional
from pydantic import BaseModel


class ContactInformation(BaseModel):
    """Model for contact information returned from Whois API."""
    
    registrant_name: Optional[str] = None
    technical_contact_name: Optional[str] = None
    administrative_contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    
    class Config:
        """Pydantic config."""
        
        json_schema_extra = {
            "example": {
                "registrant_name": "Domain Administrator",
                "technical_contact_name": "Tech Admin",
                "administrative_contact_name": "Admin Contact",
                "contact_email": "admin@example.com"
            }
        }

        