import app.schemas as schemas
import app.models as models
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status, Depends


def create_mortgage_crud(
    payload: schemas.MortgageCreateModel, db: Session = Depends(get_db)
):
    try:
        new_mortgage = models.MortgageOrm(**payload.model_dump())

        # Check whether the property exists in the DB
        property_data = (
            db.query(models.PropertyOrm)
            .filter(models.PropertyOrm.id == payload.property_id)
            .first()
        )
        if not property_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found.",
            )

        db.add(new_mortgage)
        db.commit()
        db.refresh(new_mortgage)

        mortgage_data = schemas.MortgageModel.model_validate(new_mortgage)

        return schemas.MortgageResponseModel(
            status=schemas.Status.Success,
            message="Mortgage created successfully.",
            data=mortgage_data,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A mortgage with the given details already exists.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the mortgage: {str(e)}",
        )


def get_mortgage_crud(mortgage_id: str, db: Session = Depends(get_db)):
    mortgage_data = (
        db.query(models.MortgageOrm)
        .filter(models.MortgageOrm.id == mortgage_id)
        .first()
    )

    if not mortgage_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mortgage not found.",
        )

    try:
        return schemas.MortgageResponseModel(
            status=schemas.Status.Success,
            message="Mortgage retrieved successfully.",
            data=schemas.MortgageModel.model_validate(mortgage_data),
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the mortgage.",
        ) from e


def update_mortgage_crud(
    mortgage_id: str, payload: schemas.MortgageUpdateModel, db: Session
):
    mortgage_query = db.query(models.MortgageOrm).filter(
        models.MortgageOrm.id == mortgage_id
    )
    db_mortgage = mortgage_query.first()

    if not db_mortgage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mortgage not found."
        )

    try:
        # Prepare update data from the payload, only including fields that are set
        update_data = payload.model_dump(exclude_unset=True)
        if update_data:
            mortgage_query.update(update_data, synchronize_session="evaluate")
            db.commit()
            db.refresh(db_mortgage)

            # Convert the updated ORM model back to a Pydantic model
            return schemas.MortgageResponseModel(
                status=schemas.Status.Success,
                message="Mortgage updated successfully.",
                data=schemas.MortgageModel.model_validate(db_mortgage),
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
            detail="A mortgage with the given details already exists.",
        ) from e
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the mortgage: {str(e)}",
        ) from e


def delete_mortgage_crud(mortgage_id: str, db: Session = Depends(get_db)):
    try:
        mortgage_query = db.query(models.MortgageOrm).filter(
            models.MortgageOrm.id == mortgage_id
        )
        mortgage_ = mortgage_query.first()
        if not mortgage_:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No mortgage found with ID: {mortgage_id}",
            )
        mortgage_query.delete(synchronize_session=False)
        db.commit()
        return schemas.MortgageDeleteModel(
            id=mortgage_id,
            status=schemas.Status.Success,
            message="Mortgage deleted successfully.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the mortgage.",
        ) from e


def get_mortgages_crud(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""
):
    skip = (page - 1) * limit

    mortgages = db.query(models.MortgageOrm).limit(limit).offset(skip).all()
    return schemas.MortgageListResponseModel(
        status=schemas.Status.Success,
        message="Mortgages retrieved successfully.",
        data=[schemas.MortgageModel.model_validate(mortgage) for mortgage in mortgages],
    )
