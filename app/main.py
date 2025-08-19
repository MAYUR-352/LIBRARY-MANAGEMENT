# Entry point for the Library Management application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, users, books, borrowings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="A comprehensive library management system with user authentication and book tracking",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(borrowings.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Library Management System API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

