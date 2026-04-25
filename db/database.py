import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

#echo = True logs SQL queries
engine = create_async_engine(DATABASE_URL, echo=True)

#factory to create DB sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

#Base class for all models
Base = declarative_base()