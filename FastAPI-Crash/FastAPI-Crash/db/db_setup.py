from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432"
ASYNC_SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:amar@localhost/fastapidb"

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:amar@localhost/fastapidb"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# host=localhost;database=; Username=postgres; Password=amar;

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}, future=True
)

async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def async_get_db():
    async with AsyncSessionLocal as db:
        yield db
        await db.commit()
