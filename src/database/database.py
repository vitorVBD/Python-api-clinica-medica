from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está definida")

try:
    engine = create_async_engine(DATABASE_URL, echo=True)
except Exception as e:
    raise Exception(f"Erro ao criar engine: {str(e)}")

SessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

db = declarative_base()