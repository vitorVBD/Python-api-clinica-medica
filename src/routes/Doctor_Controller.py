from fastapi import APIRouter, Depends, HTTPException
from services.Doctor_Service import DoctorService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from database.database import engine
from auth.security import hash_password

router = APIRouter()

async def get_session():
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


@router.post("/post_doctors/")
async def create_doctor(name: str, email: str, password: str, specialty: str, phone: str, crm: str, session: AsyncSession = Depends(get_session)):
    hashed_password = hash_password(password)
    doctor_service = DoctorService(session)
    try:
        doctor = await doctor_service.create_doctor(name, email, hashed_password, specialty, phone, crm)
        return JSONResponse(content={"message": "Médico criado com sucesso"}, status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/doctors/{doctor_id}")
async def get_doctor_by_id(doctor_id: int, session: AsyncSession = Depends(get_session)):
    doctor_service = DoctorService(session)
    try:
        doctor = await doctor_service.get_doctor_by_id(doctor_id)
        return doctor
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/doctors/crm/{crm}")
async def get_doctor_by_crm(crm: str, session: AsyncSession = Depends(get_session)):
    doctor_service = DoctorService(session)
    try:
        doctor = await doctor_service.get_doctor_by_crm(crm)
        return doctor
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/doctors/")
async def get_all_doctors(session: AsyncSession = Depends(get_session)):
    doctor_service = DoctorService(session)
    try:
        doctors = await doctor_service.get_all_doctors()
        return doctors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/doctors/{doctor_id}")
async def update_doctor(doctor_id: int, name: str = None, email: str = None, specialty: str = None,
                         phone: str = None, crm: str = None, session: AsyncSession = Depends(get_session)):
    doctor_service = DoctorService(session)
    try:
        updated_doctor = await doctor_service.update_doctor(doctor_id, name, email, specialty, phone, crm)
        return updated_doctor
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/doctors/{doctor_id}")
async def delete_doctor(doctor_id: int, session: AsyncSession = Depends(get_session)):
    doctor_service = DoctorService(session)
    try:
        await doctor_service.delete_doctor(doctor_id)
        return JSONResponse(content={"message": "Médico deletado com sucesso"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))