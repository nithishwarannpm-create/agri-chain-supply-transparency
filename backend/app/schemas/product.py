from datetime import date

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    crop_name: str = Field(..., min_length=1)
    quantity: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1)
    farmer_id: str = Field(..., min_length=1)
    harvest_date: date
    location: str = Field(..., min_length=1)
    quality_grade: str | None = None


class ProductResponse(ProductCreate):
    product_id: str