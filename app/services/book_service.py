# Book service
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.book import Book, BookStatus
from app.schemas.book import BookCreate, BookUpdate
from typing import Optional, List


def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()


def get_book_by_isbn(db: Session, isbn: str) -> Optional[Book]:
    return db.query(Book).filter(Book.isbn == isbn).first()


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Book]:
    query = db.query(Book)

    if category:
        query = query.filter(Book.category == category)

    if search:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%"),
                Book.isbn.ilike(f"%{search}%"),
            )
        )

    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(**book.dict(), available_copies=book.total_copies)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book_update: BookUpdate) -> Optional[Book]:
    db_book = get_book(db, book_id)
    if db_book:
        update_data = book_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)

        # Update available copies if total copies changed
        if "total_copies" in update_data:
            borrowed_count = len(
                [b for b in db_book.borrowings if b.status == "active"]
            )
            db_book.available_copies = max(0, db_book.total_copies - borrowed_count)

        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False


def update_book_availability(db: Session, book_id: int, change: int):
    """Update available copies count (+1 for return, -1 for borrow)"""
    db_book = get_book(db, book_id)
    if db_book:
        db_book.available_copies = max(0, db_book.available_copies + change)
        if db_book.available_copies == 0:
            db_book.status = BookStatus.BORROWED
        elif db_book.available_copies > 0:
            db_book.status = BookStatus.AVAILABLE
        db.commit()
        db.refresh(db_book)
    return db_book
