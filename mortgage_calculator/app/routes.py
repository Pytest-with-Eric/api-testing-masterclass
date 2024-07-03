from typing import Dict

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import app.schemas as schemas
from app.crud.mortgage_crud import (create_mortgage_crud, delete_mortgage_crud,
                                    get_mortgage_crud, get_mortgages_crud,
                                    update_mortgage_crud)
from app.crud.property_crud import (create_property_crud, delete_property_crud,
                                    get_properties_crud, get_property_crud,
                                    update_property_crud)
from app.custom.db_queries import get_mortgage_payment
from app.database import get_db

router = APIRouter()


@router.post(
    "/property",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PropertyResponseModel,
)
def create_property(
    property: schemas.PropertyCreateModel, db: Session = Depends(get_db)
) -> schemas.PropertyResponseModel:
    """
    Create a new property.
    """
    return create_property_crud(payload=property, db=db)


@router.get(
    "/property/{property_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PropertyResponseModel,
)
def get_property(
    property_id: str, db: Session = Depends(get_db)
) -> schemas.PropertyResponseModel:
    """
    Get a property by ID.
    """
    return get_property_crud(property_id=property_id, db=db)


@router.patch(
    "/property/{property_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.PropertyResponseModel,
)
def update_property(
    property_id: str,
    property: schemas.PropertyUpdateModel,
    db: Session = Depends(get_db),
) -> schemas.PropertyResponseModel:
    """
    Update a property by ID.
    """
    return update_property_crud(property_id=property_id, payload=property, db=db)


@router.delete(
    "/property/{property_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.PropertyDeleteModel,
)
def delete_property(
    property_id: str, db: Session = Depends(get_db)
) -> schemas.PropertyDeleteModel:
    """
    Delete a property by ID.
    """
    return delete_property_crud(property_id=property_id, db=db)


@router.get(
    "/property",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PropertyListResponseModel,
)
def get_properties(db: Session = Depends(get_db)) -> schemas.PropertyListResponseModel:
    """
    Get all properties.
    """
    return get_properties_crud(db=db)


@router.post(
    "/mortgage",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MortgageResponseModel,
)
def create_mortgage(
    mortgage: schemas.MortgageCreateModel, db: Session = Depends(get_db)
) -> schemas.MortgageResponseModel:
    """
    Create a new mortgage.
    """
    return create_mortgage_crud(payload=mortgage, db=db)


@router.get(
    "/mortgage/{mortgage_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MortgageResponseModel,
)
def get_mortgage(
    mortgage_id: str, db: Session = Depends(get_db)
) -> schemas.MortgageResponseModel:
    """
    Get a mortgage by ID.
    """
    return get_mortgage_crud(mortgage_id=mortgage_id, db=db)


@router.patch(
    "/mortgage/{mortgage_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.MortgageResponseModel,
)
def update_mortgage(
    mortgage_id: str,
    mortgage: schemas.MortgageUpdateModel,
    db: Session = Depends(get_db),
) -> schemas.MortgageResponseModel:
    """
    Update a mortgage by ID.
    """
    return update_mortgage_crud(mortgage_id=mortgage_id, payload=mortgage, db=db)


@router.delete(
    "/mortgage/{mortgage_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.MortgageDeleteModel,
)
def delete_mortgage(
    mortgage_id: str, db: Session = Depends(get_db)
) -> schemas.MortgageDeleteModel:
    """
    Delete a mortgage by ID.
    """
    return delete_mortgage_crud(mortgage_id=mortgage_id, db=db)


@router.get(
    "/mortgage",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MortgageListResponseModel,
)
def get_mortgages(db: Session = Depends(get_db)) -> schemas.MortgageListResponseModel:
    """
    Get all mortgages.
    """
    return get_mortgages_crud(db=db)


@router.post("/mortgage/{mortgage_id}/payment", response_model=Dict[str, str | float])
def calculate_mortgage_payment(
    mortgage_id: str, db: Session = Depends(get_db)
) -> Dict[str, str | float]:
    """
    Retrieve the monthly payment for a given mortgage.
    """
    return get_mortgage_payment(mortgage_id, db)
