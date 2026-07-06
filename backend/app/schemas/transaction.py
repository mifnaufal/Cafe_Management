from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactionItemCreate(BaseModel):
    product_id: int
    quantity: int


class TransactionCreate(BaseModel):
    items: list[TransactionItemCreate]
    payment_method: str = "cash"
    notes: Optional[str] = None


class CashierRef(BaseModel):
    id: int
    full_name: str

    class Config:
        from_attributes = True


class TransactionItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    price_at_time: int
    quantity: int
    subtotal: int

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    id: int
    transaction_number: str
    total_amount: int
    payment_method: str
    cashier: Optional[CashierRef] = None
    items: list[TransactionItemResponse] = []
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PaginatedTransactions(BaseModel):
    items: list[TransactionResponse]
    total: int
    page: int
    limit: int
    total_pages: int
