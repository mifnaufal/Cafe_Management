from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.crud import report as report_crud
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary")
def get_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return report_crud.get_summary(db)


@router.get("/sales-chart")
def get_sales_chart(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_crud.get_sales_chart(db, days=days)


@router.get("/top-products")
def get_top_products(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_crud.get_top_products(db, limit=limit)


@router.get("/category-breakdown")
def get_category_breakdown(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return report_crud.get_category_breakdown(db)
