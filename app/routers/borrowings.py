# Borrowings router
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.borrowing import (
    BorrowingCreate,
    BorrowingResponse,
    BorrowingDetailResponse,
)
from app.services.borrowing_service import (
    create_borrowing,
    get_user_borrowings,
    return_book,
    get_all_borrowings,
    get_overdue_borrowings,
)
from app.utils.dependencies import get_current_user, get_librarian_or_admin
from app.models.user import User

router = APIRouter(prefix="/borrowings", tags=["borrowings"])


@router.post("/", response_model=BorrowingResponse, status_code=status.HTTP_201_CREATED)
async def borrow_book(
    borrowing: BorrowingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_borrowing = create_borrowing(db, borrowing, current_user.id)
    if not db_borrowing:
        raise HTTPException(status_code=400, detail="Book not available for borrowing")
    return db_borrowing


@router.get("/my-borrowings", response_model=List[BorrowingResponse])
async def read_my_borrowings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_borrowings(db, current_user.id, skip=skip, limit=limit)


@router.get("/", response_model=List[BorrowingDetailResponse])
async def read_all_borrowings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_librarian_or_admin),
):
    return get_all_borrowings(db, skip=skip, limit=limit)


@router.get("/overdue", response_model=List[BorrowingDetailResponse])
async def read_overdue_borrowings(
    db: Session = Depends(get_db), current_user: User = Depends(get_librarian_or_admin)
):
    return get_overdue_borrowings(db)


@router.patch("/{borrowing_id}/return", response_model=BorrowingResponse)
async def return_borrowed_book(
    borrowing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    borrowing = return_book(db, borrowing_id, current_user.id)
    if not borrowing:
        raise HTTPException(
            status_code=404, detail="Borrowing not found or already returned"
        )
    return borrowing
