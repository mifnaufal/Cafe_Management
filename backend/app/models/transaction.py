from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_number = Column(String(50), unique=True, nullable=False, index=True)
    total_amount = Column(Integer, nullable=False)
    payment_method = Column(String(50), default="cash")
    cashier_id = Column(Integer, ForeignKey("users.id"))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cashier = relationship("User", lazy="joined")
    items = relationship("TransactionItem", back_populates="transaction", lazy="joined", cascade="all, delete-orphan")
