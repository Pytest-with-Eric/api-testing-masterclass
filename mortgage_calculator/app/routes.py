from fastapi import status, APIRouter, Depends
from app import crud
import app.schemas as schemas
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PropertyResponse
)
def create_property(property: schemas.PropertyCreate, db: Session = Depends(get_db)):
    return crud.property_crud.create_property(db=db, property=property)
