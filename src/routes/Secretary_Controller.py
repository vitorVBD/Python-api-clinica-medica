from fastapi import APIRouter, Depends, HTTPException
from services.Secretary_Service import Secretary_Service
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from database.database import engine
from auth.security import hash_password

router = APIRouter()

async def get_session():
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session

@router.post("/secretaries/")
async def create_secretary(name: str, birth_date: str, password: str, phone: str, email: str, session: AsyncSession = Depends(get_session)):
    hashed_password = hash_password(password)
    secretary_service = Secretary_Service(session)
    try:
        secretary = await secretary_service.create_secretary(name, birth_date, hashed_password, phone, email)
        return JSONResponse(content={"message": "Secretário criado com sucesso"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/secretaries/{secretary_id}")
async def get_secretary_by_id(secretary_id: int, session: AsyncSession = Depends(get_session)):
    secretary_service = Secretary_Service(session)
    try:
        secretary = await secretary_service.get_secretary_by_id(secretary_id)
        return secretary
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/secretaries/email/{email}")
async def get_secretary_by_email(email: str, session: AsyncSession = Depends(get_session)):
    secretary_service = Secretary_Service(session)
    try:
        secretary = await secretary_service.get_secretary_by_email(email)
        return secretary
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/secretaries/")
async def get_all_secretaries(session: AsyncSession = Depends(get_session)):
    secretary_service = Secretary_Service(session)
    try:
        secretaries = await secretary_service.get_all_secretaries()
        return secretaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/secretaries/{secretary_id}")
async def update_secretary(secretary_id: int, name: str = None, birth_date: str = None, hashed_password: str = None, phone: str = None, email: str = None, session: AsyncSession = Depends(get_session)):
    secretary_service = Secretary_Service(session)
    try:
        updated_secretary = await secretary_service.update_secretary(secretary_id, name, birth_date, hashed_password, phone, email)
        return updated_secretary
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/secretaries/{secretary_id}")
async def delete_secretary(secretary_id: int, session: AsyncSession = Depends(get_session)):
    secretary_service = Secretary_Service(session)
    try:
        await secretary_service.delete_secretary(secretary_id)
        return JSONResponse(content={"message": "Secretário deletado com sucesso"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))