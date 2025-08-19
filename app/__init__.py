# Library Management System - FastAPI
#
# Project Structure
# library_management/
# ├── app/
# │   ├── __init__.py
# │   ├── main.py
# │   ├── config.py
# │   ├── database.py
# │   ├── models/
# │   │   ├── __init__.py
# │   │   ├── user.py
# │   │   ├── book.py
# │   │   └── borrowing.py
# │   ├── schemas/
# │   │   ├── __init__.py
# │   │   ├── user.py
# │   │   ├── book.py
# │   │   └── borrowing.py
# │   ├── routers/
# │   │   ├── __init__.py
# │   │   ├── auth.py
# │   │   ├── users.py
# │   │   ├── books.py
# │   │   └── borrowings.py
# │   ├── services/
# │   │   ├── __init__.py
# │   │   ├── auth_service.py
# │   │   ├── user_service.py
# │   │   ├── book_service.py
# │   │   └── borrowing_service.py
# │   └── utils/
# │       ├── __init__.py
# │       ├── auth.py
# │       └── dependencies.py
# ├── requirements.txt
# ├── .env
# └── README.md
#
# File Contents
#
# requirements.txt
# fastapi==0.104.1
# uvicorn==0.24.0
# sqlalchemy==2.0.23
# alembic==1.12.1
# psycopg2-binary==2.9.9
# python-jose[cryptography]==3.3.0
# python-multipart==0.0.6
# passlib[bcrypt]==1.7.4
# python-decouple==3.8
# pydantic[email]==2.5.0
#
# .env
# DATABASE_URL=postgresql://username:password@localhost/library_db
# SECRET_KEY=your-secret-key-here
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30
#
# Setup Instructions
# 1. Install Dependencies:
#    pip install -r requirements.txt
# 2. Setup Database:
#    - Create PostgreSQL database
#    - Update .env file with your database credentials
# 3. Run Database Migrations:
#    alembic init alembic
#    alembic revision --autogenerate -m "Initial migration"
#    alembic upgrade head
# 4. Create Admin User (Run this script once):
#    # create_admin.py
#    from sqlalchemy.orm import Session
#    from app.database import SessionLocal
#    from app.models.user import User, UserRole
#    from app.utils.auth import get_password_hash
#    def create_admin():
#        db = SessionLocal()
#        admin = User(
#            email="admin@library.com",
#            username="admin",
#            full_name="System Administrator",
#            hashed_password=get_password_hash("admin123"),
#            role=UserRole.ADMIN,
#            is_active=True
#        )
#        db.add(admin)
#        db.commit()
#        print("Admin user created successfully!")
#        db.close()
#    if __name__ == "__main__":
#        create_admin()
# 5. Run the Application:
#    uvicorn app.main:app --reload
#
# API Endpoints
# Authentication
#   POST /auth/login - Login user
# Users
#   POST /users/ - Create user (Admin only)
#   GET /users/ - Get all users (Admin only)
#   GET /users/me - Get current user profile
#   GET /users/{user_id} - Get user by ID (Admin only)
#   PUT /users/{user_id} - Update user (Admin only)
#   DELETE /users/{user_id} - Delete user (Admin only)
# Books
#   POST /books/ - Add new book (Librarian/Admin)
#   GET /books/ - Get all books (with search and filter)
#   GET /books/{book_id} - Get book details
#   PUT /books/{book_id} - Update book (Librarian/Admin)
#   DELETE /books/{book_id} - Delete book (Librarian/Admin)
# Borrowings
#   POST /borrowings/ - Borrow a book
#   GET /borrowings/my-borrowings - Get user's borrowings
#   GET /borrowings/ - Get all borrowings (Librarian/Admin)
#   GET /borrowings/overdue - Get overdue borrowings (Librarian/Admin)
#   PATCH /borrowings/{borrowing_id}/return - Return a book
#
# Features
# ✅ User Management: Registration, authentication, role-based access
# ✅ Book Management: CRUD operations, search, categorization
# ✅ Borrowing System: Book checkout, return, due date tracking
# ✅ Authentication: JWT-based authentication with role permissions
# ✅ Database Models: SQLAlchemy ORM with proper relationships
# ✅ API Documentation: Auto-generated with FastAPI/OpenAPI
# ✅ Search & Filter: Book search by title, author, ISBN, category
# ✅ Overdue Tracking: Automatic overdue detection
# ✅ Inventory Management: Available copies tracking
#
# User Roles
# Admin: Full system access
# Librarian: Manage books and view all borrowings
# Member: Borrow/return books, view own borrowings
#
# Access the API documentation at: http://localhost:8000/docs
