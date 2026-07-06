from datetime import datetime, timezone, timedelta, date

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.transaction import Transaction
from app.models.transaction_item import TransactionItem
from app.models.product import Product
from app.models.category import Category


def _get_period_summary(db: Session, start_date: datetime) -> dict:
    result = (
        db.query(
            func.coalesce(func.sum(Transaction.total_amount), 0).label("total_sales"),
            func.count(Transaction.id).label("total_transactions"),
        )
        .filter(Transaction.created_at >= start_date)
        .first()
    )
    total_sales = result.total_sales
    total_transactions = result.total_transactions
    avg = round(total_sales / total_transactions, 2) if total_transactions > 0 else 0
    return {
        "total_sales": total_sales,
        "total_transactions": total_transactions,
        "average_transaction": avg,
    }


def get_summary(db: Session) -> dict:
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())
    month_start = today_start.replace(day=1)

    return {
        "today": _get_period_summary(db, today_start),
        "this_week": _get_period_summary(db, week_start),
        "this_month": _get_period_summary(db, month_start),
    }


def get_sales_chart(db: Session, days: int = 7) -> list[dict]:
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)

    rows = (
        db.query(
            func.date(Transaction.created_at).label("date"),
            func.coalesce(func.sum(Transaction.total_amount), 0).label("total_sales"),
            func.count(Transaction.id).label("transaction_count"),
        )
        .filter(Transaction.created_at >= start_date)
        .group_by(func.date(Transaction.created_at))
        .order_by(func.date(Transaction.created_at))
        .all()
    )

    return [
        {
            "date": str(row.date),
            "total_sales": row.total_sales,
            "transaction_count": row.transaction_count,
        }
        for row in rows
    ]


def get_top_products(db: Session, limit: int = 5) -> list[dict]:
    rows = (
        db.query(
            TransactionItem.product_id,
            TransactionItem.product_name,
            func.sum(TransactionItem.quantity).label("total_quantity"),
            func.sum(TransactionItem.subtotal).label("total_sales"),
        )
        .group_by(TransactionItem.product_id, TransactionItem.product_name)
        .order_by(func.sum(TransactionItem.subtotal).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "product_id": row.product_id,
            "product_name": row.product_name,
            "total_quantity": row.total_quantity,
            "total_sales": row.total_sales,
        }
        for row in rows
    ]


def get_category_breakdown(db: Session) -> list[dict]:
    rows = (
        db.query(
            Category.id.label("category_id"),
            Category.name.label("category_name"),
            func.coalesce(func.sum(TransactionItem.subtotal), 0).label("total_sales"),
            func.count(func.distinct(Transaction.id)).label("total_transactions"),
        )
        .join(Product, Product.category_id == Category.id, isouter=True)
        .join(TransactionItem, TransactionItem.product_id == Product.id, isouter=True)
        .join(Transaction, Transaction.id == TransactionItem.transaction_id, isouter=True)
        .group_by(Category.id, Category.name)
        .order_by(Category.name)
        .all()
    )

    return [
        {
            "category_id": row.category_id,
            "category_name": row.category_name,
            "total_sales": row.total_sales,
            "total_transactions": row.total_transactions,
        }
        for row in rows
    ]
