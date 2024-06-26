from enum import Enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class Status(Enum):
    Success = "Success"
    Error = "Error"


class PropertyBaseModel(BaseModel):
    purchase_price: Optional[float] = Field(
        ...,
        json_schema_extra={
            "example": 300000.00,
            "description": "The purchase price of the property",
        },
    )

    rental_income: Optional[float] = Field(
        ...,
        json_schema_extra={
            "example": 1500.00,
            "description": "Monthly rental income from the property",
        },
    )
    renovation_cost: Optional[float] = Field(
        ...,
        json_schema_extra={
            "example": 20000.00,
            "description": "Cost of renovation for the property",
        },
    )
    property_name: Optional[str] = Field(
        ...,
        json_schema_extra={
            "example": "Property 1",
            "description": "Name of the property",
        },
    )

    model_config = ConfigDict(from_attributes=True)


class PropertyCreateModel(PropertyBaseModel):
    purchase_price: float
    rental_income: float
    renovation_cost: float
    property_name: str


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


# # Mortgage Schemas
# class MortgageBaseModel(BaseModel):
#     loan_to_value: float = Field(
#         ..., description="Loan to value ratio of the mortgage", example=80.0
#     )
#     interest_rate: float = Field(
#         ..., description="Interest rate for the mortgage", example=3.5
#     )
#     mortgage_type: str = Field(
#         ...,
#         description="Type of mortgage (interest_only or capital_repayment)",
#         example="capital_repayment",
#     )


# class MortgageCreateModel(MortgageBaseModel):
#     property_id: UUID


# class MortgageResponseModel(BaseModel):
#     id: UUID
#     status: Status
#     mortgage: MortgageBaseModel
#     createdAt: datetime
#     updatedAt: Optional[datetime]


# # Cost Schemas
# class CostBaseModel(BaseModel):
#     admin_costs: float = Field(
#         ...,
#         description="Administrative costs associated with the property",
#         example=500.00,
#     )
#     management_fees: float = Field(
#         ..., description="Monthly management fees", example=100.00
#     )


# class CostCreateModel(CostBaseModel):
#     property_id: UUID


# class CostResponseModel(BaseModel):
#     id: UUID
#     status: Status
#     cost: CostBaseModel
#     createdAt: datetime
#     updatedAt: Optional[datetime]


# # Combined Response Schemas
# class PropertyDetailResponseModel(BaseModel):
#     status: Status
#     property: PropertyBaseModel
#     mortgages: List[MortgageBaseModel]
#     costs: List[CostBaseModel]


# # General API Responses
# class ApiResponseModel(BaseModel):
#     status: Status
#     message: str
