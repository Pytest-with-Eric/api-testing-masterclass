from sqlalchemy.orm import Session
from app.models import MortgageOrm, PropertyOrm
from fastapi import HTTPException, status
from app.custom.calculations import (
    calculate_interest_only_payment,
    calculate_repayment_mortgage_payment,
)
from app.schemas import MortgageType


def get_mortgage_payment(mortgage_id: str, db: Session):
    mortgage = db.query(MortgageOrm).filter(MortgageOrm.id == mortgage_id).first()
    if not mortgage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mortgage not found."
        )

    property = (
        db.query(PropertyOrm).filter(PropertyOrm.id == mortgage.property_id).first()
    )
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated property not found.",
        )

    if mortgage.mortgage_type == MortgageType.interest_only.value:
        monthly_payment = calculate_interest_only_payment(
            property.purchase_price, mortgage.interest_rate
        )
    elif mortgage.mortgage_type == MortgageType.repayment.value:
        # Assuming a fixed loan term, e.g., 30 years. This could also be dynamically fetched or adjusted.
        monthly_payment = calculate_repayment_mortgage_payment(
            property.purchase_price, mortgage.interest_rate, 30
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported mortgage type."
        )

    return {"mortgage_id": mortgage.id, "monthly_payment": monthly_payment}
