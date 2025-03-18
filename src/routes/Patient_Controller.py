from fastapi import APIRouter, Depends, HTTPException
from services.Patient_Service import Patient_Service
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from database.database import engine


router = APIRouter()

async def get_session():
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


@router.post("/post_patients/")
async def create_patient(name: str, cpf: str, birth_date: str, medical_insurance: str, city: str, email: str, phone: str, session: AsyncSession = Depends(get_session)):
    patient_service = Patient_Service(session)
    try:
        patient = await patient_service.create_patient(name, cpf, birth_date, medical_insurance, city, email, phone)
        return JSONResponse(content={"message": "Paciente criado com sucesso"}, status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patients/{patient_id}")
async def get_patient_by_id(patient_id: int, session: AsyncSession = Depends(get_session)):
    patient_service = Patient_Service(session)
    try:
        patient = await patient_service.get_patient_by_id(patient_id)
        return patient
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patients/cpf/{cpf}")
async def get_patient_by_cpf(cpf: str, session: AsyncSession = Depends(get_session)):
    patient_service = Patient_Service(session)
    try:
        patient = await patient_service.get_patient_by_cpf(cpf)
        return patient
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patients/")
async def get_all_patients(session: AsyncSession = Depends(get_session)):
    patient_service = Patient_Service(session)
    try:
        patients = await patient_service.get_all_patients()
        return patients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/patients/{patient_id}")
async def update_patient(patient_id: int, name: str = None, cpf: str = None, birth_date: str = None,
                         medical_insurance: str = None, city: str = None, email: str = None, phone: str = None, session: AsyncSession = Depends(get_session)):
    patient_service = Patient_Service(session)
    try:
        updated_patient = await patient_service.update_patient(patient_id, name, cpf, birth_date, medical_insurance, city, email, phone)
        return updated_patient
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int, session: AsyncSession = Depends(get_session)):
    patient_service = Patient_Service(session)
    try:
        await patient_service.delete_patient(patient_id)
        return JSONResponse(content={"message": "Paciente deletado com sucesso"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))