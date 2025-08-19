# Books router
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.services.book_service import (
    create_book,
    get_books,
    get_book,
    update_book,
    delete_book,
    get_book_by_isbn,
)
from app.utils.dependencies import get_current_user, get_librarian_or_admin
from app.models.user import User

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_new_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_librarian_or_admin),
):
    # Check if book with ISBN already exists
    if get_book_by_isbn(db, book.isbn):
        raise HTTPException(
            status_code=400, detail="Book with this ISBN already exists"
        )

    return create_book(db, book)


@router.get("/", response_model=List[BookResponse])
async def read_books(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_books(db, skip=skip, limit=limit, category=category, search=search)


@router.get("/{book_id}", response_model=BookResponse)
async def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse)
async def update_book_endpoint(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_librarian_or_admin),
):
    book = update_book(db, book_id, book_update)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}")
async def delete_book_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_librarian_or_admin),
):
    if delete_book(db, book_id):
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
