
# Library Management System

A comprehensive Library Management System built with FastAPI, SQLAlchemy, and SQLite. It supports user authentication, book management, borrowing/returning, and role-based access control.

## Features

- **User Management:** Registration, authentication, role-based access (Admin, Librarian, Member)
- **Book Management:** CRUD operations, search, categorization
- **Borrowing System:** Book checkout, return, due date tracking
- **Authentication:** JWT-based authentication with role permissions
- **Database Models:** SQLAlchemy ORM with proper relationships
- **API Documentation:** Auto-generated with FastAPI/OpenAPI
- **Search & Filter:** Book search by title, author, ISBN, category
- **Overdue Tracking:** Automatic overdue detection
- **Inventory Management:** Available copies tracking

## Project Structure

```text
library_management/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   └── borrowing.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   └── borrowing.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── books.py
│   │   └── borrowings.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── book_service.py
│   │   └── borrowing_service.py
│   └── utils/
│       ├── __init__.py
│       ├── auth.py
│       └── dependencies.py
├── requirements.txt
├── .env
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (optional, for containerization)

### Installation

1. **Clone the repository:**
	```sh
	git clone <your-repo-url>
	cd library_management
	```

2. **Create and activate a virtual environment:**
	```sh
	python -m venv .venv
	.venv\Scripts\activate  # On Windows
	source .venv/bin/activate  # On Linux/Mac
	```

3. **Install dependencies:**
	```sh
	pip install -r requirements.txt
	```

4. **Configure environment variables:**
	Edit `.env` file as needed. For SQLite:


5. **Run the application:**
	```sh
	uvicorn app.main:app --reload
	```

6. **Access API docs:**
	- Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

### Docker Usage

1. **Build and run with Docker Compose:**
	```sh
	docker-compose up --build
	```
	SQLite is used, so no database container is required.

## API Endpoints

### Authentication
- `POST /auth/register` — Register a new user
- `POST /auth/login` — Login user

### Users
- `POST /users/` — Create user (Admin only)
- `GET /users/` — Get all users (Admin only)
- `GET /users/me` — Get current user profile
- `GET /users/{user_id}` — Get user by ID (Admin only)
- `PUT /users/{user_id}` — Update user (Admin only)
- `DELETE /users/{user_id}` — Delete user (Admin only)

### Books
- `POST /books/` — Add new book (Librarian/Admin)
- `GET /books/` — Get all books (with search and filter)
- `GET /books/{book_id}` — Get book details
- `PUT /books/{book_id}` — Update book (Librarian/Admin)
- `DELETE /books/{book_id}` — Delete book (Librarian/Admin)

### Borrowings
- `POST /borrowings/` — Borrow a book
- `GET /borrowings/my-borrowings` — Get user's borrowings
- `GET /borrowings/` — Get all borrowings (Librarian/Admin)
- `GET /borrowings/overdue` — Get overdue borrowings (Librarian/Admin)
- `PATCH /borrowings/{borrowing_id}/return` — Return a book

## User Roles

- **Admin:** Full system access
- **Librarian:** Manage books and view all borrowings
- **Member:** Borrow/return books, view own borrowings

## License

This project is licensed under the MIT License.
