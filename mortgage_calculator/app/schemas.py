from enum import Enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID


class Status(Enum):
    Success = "Success"
    Error = "Error"


# Property Schemas
class PropertyBaseModel(BaseModel):
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

    class Config:
        from_attributes = True


class PropertyModel(PropertyBaseModel):
    id: UUID
    createdAt: datetime
    updatedAt: Optional[datetime]

    class Config:
        from_attributes = True


class PropertyCreateModel(PropertyBaseModel):
    pass


class PropertyResponseModel(BaseModel):
    status: Status = Status.Success
    message: str
    data: PropertyModel

    class Config:
        from_attributes = True


# Mortgage Schemas
class MortgageBaseModel(BaseModel):
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


class MortgageCreateModel(MortgageBaseModel):
    property_id: UUID


class MortgageResponseModel(BaseModel):
    id: UUID
    status: Status
    mortgage: MortgageBaseModel
    createdAt: datetime
    updatedAt: Optional[datetime]


# Cost Schemas
class CostBaseModel(BaseModel):
    admin_costs: float = Field(
        ...,
        description="Administrative costs associated with the property",
        example=500.00,
    )
    management_fees: float = Field(
        ..., description="Monthly management fees", example=100.00
    )


class CostCreateModel(CostBaseModel):
    property_id: UUID


class CostResponseModel(BaseModel):
    id: UUID
    status: Status
    cost: CostBaseModel
    createdAt: datetime
    updatedAt: Optional[datetime]


# Combined Response Schemas
class PropertyDetailResponseModel(BaseModel):
    status: Status
    property: PropertyBaseModel
    mortgages: List[MortgageBaseModel]
    costs: List[CostBaseModel]


# General API Responses
class ApiResponseModel(BaseModel):
    status: Status
    message: str
