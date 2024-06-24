import app.schemas as schemas
import app.models as models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


def create_property_crud(payload: schemas.PropertyCreateModel, db: Session):
    try:
        new_property = models.PropertyOrm(**payload.dict())
        db.add(new_property)
        db.commit()
        db.refresh(new_property)

        property_data = schemas.PropertyModel.from_orm(new_property)

        return schemas.PropertyResponseModel(
            status=schemas.Status.Success,
            message="Property created successfully.",
            data=property_data,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A property with the given details already exists.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the property: {str(e)}",
        )


def get_property_crud(property_id: str, db: Session):
    property_data = (
        db.query(models.PropertyOrm)
        .filter(models.PropertyOrm.id == property_id)
        .first()
    )

    if property_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found.",
        )

    property_data = schemas.PropertyBaseModel.from_orm(property_data)

    return schemas.PropertyResponseModel(
        status=schemas.Status.Success,
        message="Property retrieved successfully.",
        data=property_data,
    )
