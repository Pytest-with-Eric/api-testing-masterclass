from enum import Enum
from sqlalchemy import Column, String, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType
from sqlalchemy import Enum as SQLAlchemyEnum
import uuid
from app.database import Base


class MortgageType(str, Enum):
    interest_only = "interest_only"
    repayment = "repayment"


class PropertyOrm(Base):
    __tablename__ = "properties"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    purchase_price = Column(Numeric(10, 2), nullable=False)
    rental_income = Column(Numeric(10, 2), nullable=False)
    renovation_cost = Column(Numeric(10, 2), nullable=False)
    property_name = Column(String(255), nullable=False)
    admin_costs = Column(Numeric(10, 2), nullable=False)
    management_fees = Column(Numeric(10, 2), nullable=False)

    createdAt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
    mortgages = relationship("MortgageOrm", back_populates="property")


class MortgageOrm(Base):
    __tablename__ = "mortgages"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUIDType(binary=False), ForeignKey("properties.id"))
    loan_to_value = Column(Numeric(5, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), nullable=False)
    mortgage_type = Column(SQLAlchemyEnum(MortgageType), nullable=False)
    loan_term = Column(Numeric(5, 2), nullable=True)

    property = relationship("PropertyOrm", back_populates="mortgages")

    createdAt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
