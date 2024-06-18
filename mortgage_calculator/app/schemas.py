from enum import Enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID


class Status(Enum):
    Success = "Success"
    Error = "Error"


# Property Schemas
class PropertyBase(BaseModel):
    purchase_price: float = Field(
        ..., description="The purchase price of the property", example=300000.00
    )
    rental_income: float = Field(
        ...,
        description="Monthly rental income expected from the property",
        example=1500.00,
    )
    renovation_cost: float = Field(
        ..., description="Cost of any renovations needed", example=20000.00
    )
    property_name: str = Field(
        ..., description="Name or identifier for the property", example="Downtown Condo"
    )


class PropertyCreate(PropertyBase):
    pass


class PropertyResponse(BaseModel):
    id: UUID
    status: Status
    property: PropertyBase
    createdAt: datetime
    updatedAt: Optional[datetime]


# Mortgage Schemas
class MortgageBase(BaseModel):
    loan_to_value: float = Field(
        ..., description="Loan to value ratio of the mortgage", example=80.0
    )
    interest_rate: float = Field(
        ..., description="Interest rate for the mortgage", example=3.5
    )
    mortgage_type: str = Field(
        ...,
        description="Type of mortgage (interest_only or capital_repayment)",
        example="capital_repayment",
    )


class MortgageCreate(MortgageBase):
    property_id: UUID


class MortgageResponse(BaseModel):
    id: UUID
    status: Status
    mortgage: MortgageBase
    createdAt: datetime
    updatedAt: Optional[datetime]


# Cost Schemas
class CostBase(BaseModel):
    admin_costs: float = Field(
        ...,
        description="Administrative costs associated with the property",
        example=500.00,
    )
    management_fees: float = Field(
        ..., description="Monthly management fees", example=100.00
    )


class CostCreate(CostBase):
    property_id: UUID


class CostResponse(BaseModel):
    id: UUID
    status: Status
    cost: CostBase
    createdAt: datetime
    updatedAt: Optional[datetime]


# Combined Response Schemas
class PropertyDetailResponse(BaseModel):
    status: Status
    property: PropertyBase
    mortgages: List[MortgageBase]
    costs: List[CostBase]


# General API Responses
class ApiResponse(BaseModel):
    status: Status
    message: str
