"""Pydantic Model File."""
from pydantic import BaseModel


class AddressCreate(BaseModel):
    """Pydantic class for creating new address."""    
    name: str
    latitude: float
    longitude: float


class AddressUpdate(BaseModel):
    """Pydantic class for updating existing address."""   
    name: str
    latitude: float
    longitude: float


class AddressResponse(BaseModel):
    """Pydantic class for returning response with address's value."""   
    id: int
    name: str
    latitude: float
    longitude: float


class DistanceQuery(BaseModel):
    """Pydantic class for query parameters to fetch address's value."""   
    latitude: float
    longitude: float
    distance: float

