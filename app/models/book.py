# Book model definition
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class BookStatus(enum.Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    DAMAGED = "damaged"
    LOST = "lost"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    publisher = Column(String)
    publication_year = Column(Integer)
    category = Column(String, index=True)
    description = Column(Text)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    status = Column(Enum(BookStatus), default=BookStatus.AVAILABLE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    borrowings = relationship("Borrowing", back_populates="book")
