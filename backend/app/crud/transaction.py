from typing import Optional
from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.models.transaction import Transaction
from app.models.transaction_item import TransactionItem
from app.models.product import Product
from app.schemas.transaction import TransactionCreate
from app.utils.helpers import generate_transaction_number


def get_transactions(
    db: Session,
    page: int = 1,
    limit: int = 10,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> tuple[list[Transaction], int, int]:
    query = db.query(Transaction)

    if start_date:
        query = query.filter(Transaction.created_at >= start_date)
    if end_date:
        query = query.filter(Transaction.created_at <= end_date)

    query = query.order_by(Transaction.created_at.desc())
    total = query.count()
    total_pages = max(1, (total + limit - 1) // limit)

    transactions = (
        query.options(joinedload(Transaction.items), joinedload(Transaction.cashier))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return transactions, total, total_pages


def get_transaction_by_id(db: Session, transaction_id: int) -> Optional[Transaction]:
    return (
        db.query(Transaction)
        .options(joinedload(Transaction.items), joinedload(Transaction.cashier))
        .filter(Transaction.id == transaction_id)
        .first()
    )


def create_transaction(db: Session, data: TransactionCreate, cashier_id: int) -> Transaction:
    total_amount = 0
    items_data = []

    for item in data.items:
        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .with_for_update(of=Product.__table__)
            .first()
        )

        if not product:
            raise ValueError(f"Product with id {item.product_id} not found")

        if product.stock < item.quantity:
            raise ValueError(f"Insufficient stock for {product.name}. Available: {product.stock}, requested: {item.quantity}")

        subtotal = product.price * item.quantity
        total_amount += subtotal

        product.stock -= item.quantity

        items_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "price_at_time": product.price,
            "quantity": item.quantity,
            "subtotal": subtotal,
        })

    transaction_number = generate_transaction_number()

    transaction = Transaction(
        transaction_number=transaction_number,
        total_amount=total_amount,
        payment_method=data.payment_method,
        cashier_id=cashier_id,
        notes=data.notes,
    )
    db.add(transaction)
    db.flush()

    for item_data in items_data:
        transaction_item = TransactionItem(
            transaction_id=transaction.id,
            **item_data,
        )
        db.add(transaction_item)

    db.commit()
    db.refresh(transaction)
    return transaction
