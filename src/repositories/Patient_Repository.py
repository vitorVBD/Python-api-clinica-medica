from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from models import Patient
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

class Patient_Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, cpf: str, birth_date: str, medical_insurance: str, city: str, email: str, phone: str) -> Patient:
        patient = Patient(
            name=name,
            cpf=cpf,
            birth_date=birth_date,
            medical_insurance=medical_insurance,
            city=city,
            email=email,
            phone=phone
        )

        try:
            self.session.add(patient)
            await self.session.commit()
            await self.session.refresh(patient)
            return patient
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(f"O CPF {cpf} ou email {email} já estão em uso")
        except Exception as e:
            await self.session.rollback()
            raise e
        
    async def get_by_id(self, patient_id: int) -> Patient:
        result = await self.session.execute(select(Patient).filter(Patient.id == patient_id))
        patient = result.scalars().first()
        if not patient:
            raise ValueError(f"Paciente com ID {patient_id} não encontrado")
        return await patient
    
    async def get_by_cpf(self, cpf: str) -> Patient:
        result = await self.session.execute(select(Patient).filter(Patient.cpf == cpf))
        patient = result.scalars().first()
        if not patient:
            raise ValueError(f"Paciente com CPF {cpf} não encontrado")
        return await patient
    
    async def get_all(self) -> list:
        result = await self.session.execute(select(Patient))
        patients = result.scalars().all()
        return await patients
    
    async def update(self, patient_id: int, name: str = None, cpf: str = None, birth_date: str = None,
                     medical_insurance: str = None, city: str = None, email: str = None, phone: str = None) -> Patient:
        patient = await self.get_by_id(patient_id)

        if name:
            patient.name = name
        if cpf:
            patient.cpf = cpf
        if birth_date:
            patient.birth_date = birth_date
        if medical_insurance:
            patient.medical_insurance = medical_insurance
        if city:
            patient.city = city
        if email:
            patient.email = email
        if phone:
            patient.phone = phone

        try:
            await self.session.commit()
            await self.session.refresh(patient)
            return patient
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(f"O CPF {cpf} ou email {email} já estão em uso")
        except Exception as e:
            await self.session.rollback()
            raise e
        
    async def delete(self, patient_id: int) -> None:
        patient = await self.get_by_id(patient_id)
        self.session.delete(patient)
        await self.session.commit()