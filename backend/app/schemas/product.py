from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    stock: int = 0
    category_id: Optional[int] = None
    image_url: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class StockUpdate(BaseModel):
    stock: int


class CategoryRef(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: int
    stock: int
    category_id: Optional[int] = None
    category: Optional[CategoryRef] = None
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedProducts(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    limit: int
    total_pages: int
