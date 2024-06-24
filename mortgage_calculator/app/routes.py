from fastapi import status, APIRouter, Depends
from app.crud.property_crud import create_property_crud
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
    return create_property_crud(payload=property, db=db)
