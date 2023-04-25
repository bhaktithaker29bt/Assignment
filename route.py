"""Route File"""
import logging

from fastapi import FastAPI, Depends, HTTPException, Request, Response
from schema import AddressResponse, AddressCreate, AddressUpdate
from database import get_db, SessionLocal
from sqlalchemy.orm import Session

from crud import creating_address, updating_address, deleting_address, fetching_address, fetching_bulk_address

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """Middleware for the HTTP requests."""
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.post("/addresses", response_model=AddressResponse, status_code = 201)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    """Endpoint for creating new address.

    Args:
        address (AddressCreate): Pydantics model for request body paramaters.
        db (Session, optional): Session variable. Defaults to Depends(get_db).

    Raises:
        HTTPException: raises 500 for internal server error.

    Returns:
        _type_: dictionary
    """    
    try:
        new_address = creating_address(address, db)
        return new_address
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.put("/addresses/{address_id}", response_model=AddressResponse, status_code = 200)
def update_address(address_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    """Endpoint for updating existing address.

    Args:
        address_id (int): Id of the address as Path Parameter.
        address (AddressUpdate): Pydantics model for request body paramaters.
        db (Session, optional): Session variable. Defaults to Depends(get_db).

    Raises:
        HTTPException: riases 404 if no such record found.
        HTTPException: raises 500 for internal server error.

    Returns:
        _type_: dictionary
    """    
    try:
        result = updating_address(address_id, address, db)
        if not result:
            raise HTTPException(status_code=404, detail="Address not found")
        else:
            return result
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete("/addresses/{address_id}", status_code=204)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """Endpoint for deleting existing address.

    Args:
        address_id (int): Id of the address as Path Parameter.
        db (Session, optional): Session variable. Defaults to Depends(get_db).

    Raises:
        HTTPException: riases 404 if no such record found.
        HTTPException: raises 500 for internal server error.

    Returns:
        _type_: dictionary
    """    
    try:
        result = deleting_address(address_id, db)
        if not result:
            raise HTTPException(status_code=404, detail="Address not found")
        else:
            return None
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/addresses/{address_id}", response_model=AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db)):
    """Endpoint for fetching existing address based on id.

    Args:
        address_id (int): Id of the address as Path Parameter.
        db (Session, optional): Session variable. Defaults to Depends(get_db).

    Raises:
        HTTPException: riases 404 if no such record found.
        HTTPException: raises 500 for internal server error.

    Returns:
        _type_: dictionary
    """    
    try:
        result = fetching_address(address_id, db)
        if not result:
            raise HTTPException(status_code=404, detail="Address not found")
        else:
            return result
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/addresses", response_model=list[AddressResponse])
def get_addresses(latitude: float, longitude: float, distance: float, db: Session = Depends(get_db)):
    """Endpoint for fetching all existing address.

    Args:
        latitude (float): value of latitude.
        longitude (float): value of longitude.
        distance (float): value of the distance.
        db (Session, optional): Session variable. Defaults to Depends(get_db).

    Raises:
        HTTPException: raises 500 for internal server error.

    Returns:
        _type_: list[dict]
    """    
    try:
        result = fetching_bulk_address(latitude, longitude, distance, db)
        return result
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")