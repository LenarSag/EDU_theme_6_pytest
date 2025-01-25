from datetime import date as PyDate, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Trading(BaseModel):
    id: int = Field(..., description="Trade id")
    exchange_product_id: str = Field(..., description="Exchange product id")
    exchange_product_name: str = Field(..., description="Exchange product name")
    oil_id: Optional[str] = Field(None, description="Oil id")
    delivery_basis_id: Optional[str] = Field(None, description="Delivery basis id")
    delivery_basis_name: Optional[str] = Field(None, description="Delivery basis name")
    delivery_type_id: Optional[str] = Field(None, description="Delivery type id")
    volume: Optional[int] = Field(None, description="Volume")
    total: Optional[int] = Field(None, description="Total")
    count: Optional[int] = Field(None, description="Count")
    date: Optional[PyDate] = Field(None, description="Oil id")
    created_on: datetime = Field(..., description="Creation datetime")
    updated_on: Optional[datetime] = Field(None, description="Update datetime")

    model_config = ConfigDict(from_attributes=True)
