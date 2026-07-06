from pydantic import BaseModel


class PeriodSummary(BaseModel):
    total_sales: int = 0
    total_transactions: int = 0
    average_transaction: float = 0


class SummaryResponse(BaseModel):
    today: PeriodSummary
    this_week: PeriodSummary
    this_month: PeriodSummary


class SalesChartData(BaseModel):
    date: str
    total_sales: int
    transaction_count: int


class TopProduct(BaseModel):
    product_id: int
    product_name: str
    total_quantity: int
    total_sales: int


class CategoryBreakdown(BaseModel):
    category_id: int
    category_name: str
    total_sales: int
    total_transactions: int
