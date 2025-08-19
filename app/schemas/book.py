# Book schema definition
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.book import BookStatus


class BookBase(BaseModel):
    isbn: str
    title: str
    author: str
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None
    total_copies: int = 1


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None
    total_copies: Optional[int] = None
    status: Optional[BookStatus] = None


class BookResponse(BookBase):
    id: int
    available_copies: int
    status: BookStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
