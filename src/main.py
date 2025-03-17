from fastapi import FastAPI, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import SessionLocal, engine

app = FastAPI()

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/test-db")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute("SELECT 1")
        return {"message": "Conexão com o banco de dados bem-sucedida!", "result": result.scalar()}

    except SQLAlchemyError as e:
        return {"message": "Erro ao conectar com o banco de dados", "error": str(e)}

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return {"message": "Erro interno do servidor", "error": str(exc)}