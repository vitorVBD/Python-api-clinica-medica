from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from repositories import Doctor_Repository
from models import Doctor
from sqlalchemy.exc import IntegrityError


class DoctorService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = Doctor_Repository(session)

    async def create_doctor(self, name: str, email: str, password: str, specialty: str, phone: str, crm: str) -> Doctor:
        try:
            doctor = await self.repository.create(name, email, password, specialty, phone, crm)
            return doctor
        except IntegrityError:
            raise ValueError(f"Email {email} ou CRM {crm} já estão em uso")
        except Exception as e:
            raise Exception(f"Erro ao criar médico: {str(e)}")

    async def get_doctor_by_id(self, doctor_id: int) -> Doctor:
        try:
            doctor = await self.repository.get_by_id(doctor_id)
            return doctor
        except ValueError:
            raise ValueError(f"Médico com ID {doctor_id} não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao buscar médico: {str(e)}")

    async def get_doctor_by_crm(self, crm: str) -> Doctor:
        try:
            doctor = await self.repository.get_by_crm(crm)
            return doctor
        except ValueError:
            raise ValueError(f"Médico com CRM {crm} não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao buscar médico pelo CRM: {str(e)}")

    async def get_all_doctors(self) -> list:
        try:
            doctors = await self.repository.get_all()
            return doctors
        except Exception as e:
            raise Exception(f"Erro ao listar médicos: {str(e)}")

    async def update_doctor(self, doctor_id: int, name: str = None, email: str = None, specialty: str = None,
                            phone: str = None, crm: str = None) -> Doctor:
        try:
            updated_doctor = await self.repository.update(doctor_id, name, email, specialty, phone, crm)
            return updated_doctor
        except ValueError:
            raise ValueError(f"Médico com ID {doctor_id} não encontrado")
        except IntegrityError:
            raise ValueError(f"O CRM {crm} ou email {email} já estão em uso")
        except Exception as e:
            raise Exception(f"Erro ao atualizar médico: {str(e)}")

    async def delete_doctor(self, doctor_id: int) -> None:
        try:
            await self.repository.delete(doctor_id)
        except ValueError:
            raise ValueError(f"Médico com ID {doctor_id} não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao deletar médico: {str(e)}")