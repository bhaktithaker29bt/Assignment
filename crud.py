"""Database crud operations file"""   
from models import Address
from geopy.distance import distance

def creating_address(address, db):
    """Method for inserting records into address table.

    Args:
        address (pydantic): required parameter's value for inserting record.
        db (db_session): Session Variable.

    Returns:
        _type_: dictionary or boolean
    """    
    new_address = Address(**address.dict())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address.__dict__

def updating_address(address_id, address, db):
    """Method for updating records of address table.

    Args:
        address_id (int): ID of the address.
        address (pydantic): required parameter's value for inserting record.
        db (db_session): Session Variable.

    Returns:
        _type_: dictionary or boolean
    """    
    existing_address = db.query(Address).filter(Address.id == address_id).first()
    if existing_address:
        existing_address.name = address.name
        existing_address.latitude = address.latitude
        existing_address.longitude = address.longitude
        db.commit()
        db.refresh(existing_address)
        return existing_address.__dict__
    else:
        return False
    
def deleting_address(address_id, db):
    """Method for deleting records of address table.

    Args:
        address_id (int): ID of the address.
        db (db_session): Session Variable.

    Returns:
        _type_: Boolean
    """    
    existing_address = db.query(Address).filter(Address.id == address_id).first()
    if existing_address:
        db.delete(existing_address)
        db.commit()
        return True
    else:
        False

def fetching_address(address_id, db):
    """Method for fetching records of address table based on Id.

    Args:
        address_id (int): ID of the address.
        db (db_session): Session Variable.

    Returns:
        _type_: dictionary or boolean
    """    
    existing_address = db.query(Address).filter(Address.id == address_id).first()
    if existing_address:
        return existing_address.__dict__
    else:
        return False
    
def fetching_bulk_address(latitude, longitude, distances, db):
    """Method for fetching all the records of address table based on latitude, longitude and distance.
    Args:
        latitude (float): value of latitude
        longitude (float): value of longitude
        distances (float): value of distance
        db (db_session): Session Variable.

    Returns:
        _type_: list[dict]
    """    
    addresses = db.query(Address).all()
    result = []
    for address in addresses:
        dist = distance((latitude, longitude), (address.latitude, address.longitude)).km
        if dist <= distances:
            result.append(address.__dict__)
    return result