from fastapi import APIRouter, HTTPException, Depends
from typing import Union, Dict, Any

from app.models.domain_info import DomainRequest, DomainInformation
from app.models.contact_info import ContactInformation
from app.services.whois_service import WhoisService

router = APIRouter(prefix="/api")


def get_whois_service() -> WhoisService:
    """Dependency injection for WhoisService."""
    return WhoisService()


@router.post("/whois", 
                response_model=Union[DomainInformation, ContactInformation],
                summary="Get domain or contact information",
                description="Get domain or contact information for a given domain name")
async def get_whois_data(
    request: DomainRequest, whois_service: WhoisService = Depends(get_whois_service)
) -> Union[DomainInformation, ContactInformation]:
    """
    Get domain or contact information for a given domain name.
    
    Args:
        request: The domain request containing the domain name and info type
        whois_service: The WhoisService dependency
        
    Returns:
        DomainInformation or ContactInformation depending on the requested info_type
        
    Raises:
        HTTPException: If the domain lookup fails
    """
    try:
        # Get the raw data from the Whois API
        whois_data = await whois_service.fetch_domain_data(request.domain_name)
        
        # Parse the data based on the requested info type
        if request.info_type.lower() == "domain":
            return whois_service.parse_domain_information(whois_data)
        elif request.info_type.lower() == "contact":
            return whois_service.parse_contact_information(whois_data)
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid info_type: {request.info_type}. Must be 'domain' or 'contact'"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", 
            response_model=Dict[str, str],
            summary="Health check endpoint",
            description="Check if the API is healthy")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Dict with status message
    """
    return {"status": "healthy"}

