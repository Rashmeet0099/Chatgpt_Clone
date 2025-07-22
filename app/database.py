from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Create the database engine using the URL from .env via settings
engine = create_engine(settings.db_url)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI routes to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

