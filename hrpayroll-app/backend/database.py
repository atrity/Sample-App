from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from typing import Generator

from config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Enable connection pool "pre-ping" feature
    pool_size=5,  # Maximum number of connections to keep in the pool
    max_overflow=10  # Maximum number of connections that can be created beyond pool_size
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

@contextmanager
def get_db() -> Generator:
    """
    Context manager for database sessions.
    Ensures that a session is always properly closed, even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def init_db() -> None:
    """
    Initialize database by creating all tables.
    Should be called when application starts.
    """
    try:
        # Import all models here to ensure they are registered with Base
        from models import Employee, User, Department, Payroll, Attendance  # These will be created next
        
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
