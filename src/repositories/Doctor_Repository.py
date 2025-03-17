from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from models import Doctor
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

class Doctor_Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, email: str, hashed_password: str, specialty: str, phone: str, crm: str) -> Doctor:
        doctor = Doctor(
            name=name,
            email=email,
            hashed_password=hashed_password,
            specialty=specialty,
            phone=phone,
            crm=crm
        )
        try:
            self.session.add(doctor)
            await self.session.commit()
            await self.session.refresh(doctor)
            return doctor
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(f"O CRM {crm} ou email {email} já estão em uso")
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_by_id(self, doctor_id: int) -> Doctor:
        result = await self.session.execute(select(Doctor).filter(Doctor.id == doctor_id))
        doctor = result.scalars().first()
        if not doctor:
            raise ValueError(f"Médico com ID {doctor_id} não encontrado")
        return await doctor

    async def get_by_crm(self, crm: str) -> Doctor:
        result = await self.session.execute(select(Doctor).filter(Doctor.crm == crm))
        doctor = result.scalars().first()
        if not doctor:
            raise ValueError(f"Médico com CRM {crm} não encontrado")
        return await doctor

    async def get_all(self) -> list:
        result = await self.session.execute(select(Doctor))
        doctors = result.scalars().all()
        return doctors

    async def update(self, doctor_id: int, name: str = None, email: str = None, specialty: str = None, 
                     phone: str = None, crm: str = None) -> Doctor:
        doctor = await self.get_by_id(doctor_id)

        if name:
            doctor.name = name
        if email:
            doctor.email = email
        if specialty:
            doctor.specialty = specialty
        if phone:
            doctor.phone = phone
        if crm:
            doctor.crm = crm

        try:
            await self.session.commit()
            await self.session.refresh(doctor)
            return doctor
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(f"O CRM {crm} ou email {email} já estão em uso")
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, doctor_id: int) -> None:
        doctor = await self.get_by_id(doctor_id)
        await self.session.delete(doctor)
        await self.session.commit()