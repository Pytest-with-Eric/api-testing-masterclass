from enum import Enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from app.models import MortgageType


class Status(Enum):
    Success = "Success"
    Error = "Error"


class PropertyBaseModel(BaseModel):
    purchase_price: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "example": 300000.00,
            "description": "The purchase price of the property",
        },
    )

    rental_income: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "example": 1500.00,
            "description": "Monthly rental income from the property",
        },
    )
    renovation_cost: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "example": 20000.00,
            "description": "Cost of renovation for the property",
        },
    )
    property_name: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "example": "Property 1",
            "description": "Name of the property",
        },
    )
    admin_costs: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "example": 500.00,
            "description": "Administrative costs associated with buying the property",
        },
    )
    management_fees: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "example": 100.00,
            "description": "Monthly management fees for the property",
        },
    )
    model_config = ConfigDict(from_attributes=True)


class PropertyCreateModel(PropertyBaseModel):
    purchase_price: float
    rental_income: float
    renovation_cost: float
    property_name: str
    admin_costs: float
    management_fees: float


class PropertyUpdateModel(PropertyBaseModel):
    pass


class PropertyModel(PropertyBaseModel):
    id: UUID
    createdAt: datetime
    updatedAt: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class PropertyResponseModel(BaseModel):
    status: Status = Status.Success
    message: str
    data: PropertyModel


class PropertyListResponseModel(BaseModel):
    status: Status = Status.Success
    message: str
    data: List[PropertyModel]


class PropertyDeleteModel(BaseModel):
    id: UUID
    status: Status = Status.Success
    message: str


# Mortgage Schemas
class MortgageBaseModel(BaseModel):
    loan_to_value: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "example": 75.0,
            "description": "Loan to value ratio for the mortgage",
        },
    )
    interest_rate: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "example": 2.5,
            "description": "Interest rate for the mortgage",
        },
    )
    mortgage_type: Optional[MortgageType] = Field(
        default=None,
        json_schema_extra={
            "example": "Repayment",
            "description": "Type of mortgage",
        },
    )
    loan_term: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "example": 30,
            "description": "Loan term in years",
        },
    )
    mortgage_amount: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "example": 225000.00,
            "description": "Amount of the mortgage. Calculated based on loan to value and purchase price.",
        },
    )

    model_config = ConfigDict(from_attributes=True)


class MortgageCreateModel(MortgageBaseModel):
    loan_to_value: float
    interest_rate: float
    loan_term: int
    mortgage_type: MortgageType
    property_id: UUID


class MortgageUpdateModel(MortgageBaseModel):
    pass


class MortgageModel(MortgageBaseModel):
    id: UUID
    createdAt: datetime
    updatedAt: Optional[datetime]
    property_id: UUID

    model_config = ConfigDict(from_attributes=True)


class MortgageResponseModel(BaseModel):
    status: Status = Status.Success
    message: str
    data: MortgageModel


class MortgageDeleteModel(BaseModel):
    id: UUID
    status: Status = Status.Success
    message: str


class MortgageListResponseModel(BaseModel):
    status: Status = Status.Success
    message: str
    data: List[MortgageModel]
