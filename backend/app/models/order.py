from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class OrderType(str, Enum):
    NEW_LINE = "new_line"
    EXISTING_LINE = "existing_line"
    CASH = "cash"

class LineType(str, Enum):
    MOBILE = "mobile"
    FIBER = "fiber"

class FinancialType(str, Enum):
    INSTALLMENT = "INSTALLMENT"
    SUBSIDY = "SUBSIDY"

class Customer(BaseModel):
    name: str
    cpr: str
    mobile: str
    preferred_language: Optional[str] = None

class LineDetails(BaseModel):
    type: LineType
    number: Optional[str] = None
    sub_number: Optional[str] = None

class Device(BaseModel):
    name: str
    variant: str
    color: str

class Plan(BaseModel):
    name: str
    selected_commitment: str  # "12", "18", or "24"

class Financial(BaseModel):
    type: FinancialType
    monthly: float
    advance: float
    upfront: float
    vat: float
    total: float

class OrderData(BaseModel):
    order_id: str
    customer: Customer
    order_type: OrderType
    line_details: LineDetails
    device: Optional[Device] = None
    plan: Optional[Plan] = None
    financial: Financial
    accessories: List[str] = []
    credit_control_options: List[str] = []

