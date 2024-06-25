import app.schemas as schemas
import app.models as models
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status, Depends


def create_property_crud(
    payload: schemas.PropertyCreateModel, db: Session = Depends(get_db)
):
    try:
        new_property = models.PropertyOrm(**payload.model_dump())
        db.add(new_property)
        db.commit()
        db.refresh(new_property)

        property_data = schemas.PropertyModel.model_validate(new_property)

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


def get_property_crud(property_id: str, db: Session = Depends(get_db)):
    property_data = (
        db.query(models.PropertyOrm)
        .filter(models.PropertyOrm.id == property_id)
        .first()
    )

    if not property_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found.",
        )

    try:
        return schemas.PropertyResponseModel(
            status=schemas.Status.Success,
            message="Property retrieved successfully.",
            data=schemas.PropertyModel.model_validate(property_data),
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the property.",
        ) from e


def update_property_crud(
    property_id: str, payload: schemas.PropertyUpdateModel, db: Session
):
    property_query = db.query(models.PropertyOrm).filter(
        models.PropertyOrm.id == property_id
    )
    db_property = property_query.first()

    if not db_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Property not found."
        )

    try:
        # Prepare update data from the payload, only including fields that are set
        update_data = payload.dict(exclude_unset=True)
        if update_data:
            property_query.update(update_data, synchronize_session="evaluate")
            db.commit()
            db.refresh(db_property)

            # Convert the updated ORM model back to a Pydantic model
            return schemas.PropertyResponseModel(
                status=schemas.Status.Success,
                message="Property updated successfully.",
                data=schemas.PropertyModel.model_validate(db_property),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields provided for update.",
            )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A property with the given details already exists.",
        ) from e
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the property: {str(e)}",
        ) from e


def delete_property_crud(property_id: str, db: Session = Depends(get_db)):
    try:
        property_query = db.query(models.PropertyOrm).filter(
            models.PropertyOrm.id == property_id
        )
        property_ = property_query.first()
        if not property_:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No property found with ID: {property_id}",
            )
        property_query.delete(synchronize_session=False)
        db.commit()
        return schemas.PropertyDeleteModel(
            id=property_id,
            status=schemas.Status.Success,
            message="Property deleted successfully.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the property.",
        ) from e


def get_properties_crud(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""
):
    skip = (page - 1) * limit

    properties = db.query(models.PropertyOrm).limit(limit).offset(skip).all()
    return schemas.PropertyListResponseModel(
        status=schemas.Status.Success,
        message="Properties retrieved successfully.",
        data=[
            schemas.PropertyModel.model_validate(property) for property in properties
        ],
    )
