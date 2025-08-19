# Borrowing service
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from app.models.borrowing import Borrowing, BorrowingStatus
from app.models.book import Book
from app.schemas.borrowing import BorrowingCreate
from app.services.book_service import update_book_availability
from typing import Optional, List


def get_borrowing(db: Session, borrowing_id: int) -> Optional[Borrowing]:
    return (
        db.query(Borrowing)
        .options(joinedload(Borrowing.user), joinedload(Borrowing.book))
        .filter(Borrowing.id == borrowing_id)
        .first()
    )


def get_user_borrowings(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Borrowing]:
    return (
        db.query(Borrowing)
        .options(joinedload(Borrowing.book))
        .filter(Borrowing.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_borrowings(db: Session, skip: int = 0, limit: int = 100) -> List[Borrowing]:
    return (
        db.query(Borrowing)
        .options(joinedload(Borrowing.user), joinedload(Borrowing.book))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_borrowing(
    db: Session, borrowing: BorrowingCreate, user_id: int
) -> Optional[Borrowing]:
    # Check if book is available
    book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    if not book or book.available_copies <= 0:
        return None

    # Create borrowing record
    due_date = datetime.utcnow() + timedelta(days=14)  # 2 weeks default
    db_borrowing = Borrowing(
        user_id=user_id,
        book_id=borrowing.book_id,
        due_date=due_date,
        notes=borrowing.notes,
    )

    db.add(db_borrowing)

    # Update book availability
    update_book_availability(db, borrowing.book_id, -1)

    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


def return_book(db: Session, borrowing_id: int, user_id: int) -> Optional[Borrowing]:
    borrowing = (
        db.query(Borrowing)
        .filter(
            Borrowing.id == borrowing_id,
            Borrowing.user_id == user_id,
            Borrowing.status == BorrowingStatus.ACTIVE,
        )
        .first()
    )

    if borrowing:
        borrowing.returned_at = datetime.utcnow()
        borrowing.status = BorrowingStatus.RETURNED

        # Update book availability
        update_book_availability(db, borrowing.book_id, 1)

        db.commit()
        db.refresh(borrowing)

    return borrowing


def get_overdue_borrowings(db: Session) -> List[Borrowing]:
    return (
        db.query(Borrowing)
        .options(joinedload(Borrowing.user), joinedload(Borrowing.book))
        .filter(
            Borrowing.status == BorrowingStatus.ACTIVE,
            Borrowing.due_date < datetime.utcnow(),
        )
        .all()
    )
