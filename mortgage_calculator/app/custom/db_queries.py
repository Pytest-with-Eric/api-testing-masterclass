from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.custom.calculations import (calculate_interest_only_payment,
                                     calculate_repayment_mortgage_payment)
from app.models import MortgageOrm, PropertyOrm
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
            mortgage.mortgage_amount, mortgage.interest_rate
        )
    elif mortgage.mortgage_type == MortgageType.repayment.value:
        # Assuming a fixed loan term, e.g., 30 years. This could also be dynamically fetched or adjusted.
        monthly_payment = calculate_repayment_mortgage_payment(
            mortgage.mortgage_amount, mortgage.interest_rate, mortgage.loan_term
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported mortgage type."
        )

    return {"mortgage_id": str(mortgage.id), "monthly_payment": float(monthly_payment)}
