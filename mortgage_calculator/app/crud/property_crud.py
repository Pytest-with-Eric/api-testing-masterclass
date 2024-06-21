import app.schemas as schemas
import app.models as models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, status
from app.database import get_db


def create_property(payload: schemas.PropertyCreate, db: Session = Depends(get_db)):
    try:
        # Create a new property instance from the payload
        new_property = models.Property(**payload.model_dump())
        db.add(new_property)
        db.commit()
        db.refresh(new_property)

    except IntegrityError as e:
        db.rollback()
        # Log the error or handle it as needed
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A property with the given details already exists.",
        ) from e
    except Exception as e:
        db.rollback()
        # Handle other types of database errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the property.",
        ) from e

    # Convert the SQLAlchemy model instance to a Pydantic model
    return schemas.PropertyResponse.from_orm(new_property)
