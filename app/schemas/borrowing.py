# Borrowing schema definition
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.borrowing import BorrowingStatus
from app.schemas.user import UserResponse
from app.schemas.book import BookResponse


class BorrowingBase(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime
    notes: Optional[str] = None


class BorrowingCreate(BaseModel):
    book_id: int
    notes: Optional[str] = None


class BorrowingUpdate(BaseModel):
    due_date: Optional[datetime] = None
    status: Optional[BorrowingStatus] = None
    notes: Optional[str] = None


class BorrowingResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: Optional[datetime] = None
    status: BorrowingStatus
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class BorrowingDetailResponse(BorrowingResponse):
    user: UserResponse
    book: BookResponse
