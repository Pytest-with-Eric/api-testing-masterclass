from fastapi import status, APIRouter, Depends
from app.crud.property_crud import (
    create_property_crud,
    get_property_crud,
    update_property_crud,
    delete_property_crud,
    get_properties_crud,
)
import app.schemas as schemas
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


@router.post(
    "/property",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PropertyResponseModel,
)
def create_property(
    property: schemas.PropertyCreateModel, db: Session = Depends(get_db)
):
    """
    Create a new property.
    """
    return create_property_crud(payload=property, db=db)


@router.get(
    "/property/{property_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PropertyResponseModel,
)
def get_property(property_id: str, db: Session = Depends(get_db)):
    """
    Get a property by ID.
    """
    return get_property_crud(property_id=property_id, db=db)


@router.put(
    "/property/{property_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.PropertyResponseModel,
)
def update_property(
    property_id: str,
    property: schemas.PropertyUpdateModel,
    db: Session = Depends(get_db),
):
    """
    Update a property by ID.
    """
    return update_property_crud(property_id=property_id, payload=property, db=db)


@router.delete(
    "/property/{property_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.PropertyDeleteModel,
)
def delete_property(property_id: str, db: Session = Depends(get_db)):
    """
    Delete a property by ID.
    """
    return delete_property_crud(property_id=property_id, db=db)


@router.get(
    "/property",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PropertyListResponseModel,
)
def get_properties(db: Session = Depends(get_db)):
    """
    Get all properties.
    """
    return get_properties_crud(db=db)
