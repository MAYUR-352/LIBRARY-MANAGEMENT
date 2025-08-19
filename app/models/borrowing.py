# Borrowing model definition
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class BorrowingStatus(enum.Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"


class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrowed_at = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=False)
    returned_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(BorrowingStatus), default=BorrowingStatus.ACTIVE)
    notes = Column(Text)

    # Relationships
    user = relationship("User", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")
