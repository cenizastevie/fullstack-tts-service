from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from config import settings

# Database Configuration
DATABASE_URL = settings.database_url

# SQLAlchemy Setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Shared Session Handler
def _session_handler():
    """
    Handles the creation, commit/rollback, and cleanup of a database session.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Commit if no exceptions occur
    except Exception:
        db.rollback()  # Rollback on error
        raise
    finally:
        db.close()  # Always close the session

# Generator for FastAPI Dependencies
def get_db():
    """
    Generator for providing database sessions in FastAPI.
    """
    yield from _session_handler()

# Context Manager for Non-FastAPI Use Cases
@contextmanager
def get_db_session():
    """
    Context manager for providing database sessions outside FastAPI.
    """
    generator = _session_handler()
    try:
        db = next(generator)  # Start the session
        yield db
        next(generator, None)  # Cleanup
    except Exception as e:
        generator.throw(e)  # Propagate exceptions to the handler
        raise
