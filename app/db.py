from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import declarative_base

# Define the database connection URL for SQLite
# Note the 'sqlite+aiosqlite' prefix for async support
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

# Create the asynchronous database engine
engine: AsyncEngine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
)

# Create an async session class
SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Create the Base class for your models
Base = declarative_base()

# Define the async session_scope context manager
@asynccontextmanager
async def session_scope():
    """Provides an asynchronous transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
