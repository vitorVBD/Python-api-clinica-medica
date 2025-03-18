from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from repositories import Patient_Repository
from repositories.Patient_Repository import Patient
from sqlalchemy.exc import IntegrityError


class PatientService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = Patient_Repository(session)

    async def create_patient(self, name: str, cpf: str, birth_date: str, medical_insurance: str, city: str, email: str, phone: str) -> Patient:
        try:
            patient = await self.repository.create(name, cpf, birth_date, medical_insurance, city, email, phone)
            return patient
        except IntegrityError:
            raise ValueError(f"CPF {cpf} ou email {email} já estão em uso")
        except Exception as e:
            raise Exception(f"Erro ao criar paciente: {str(e)}")
        
    async def get_patient_by_id(self, patient_id: int) -> Patient:
        try:
            patient = await self.repository.get_by_id(patient_id)
            return patient
        except ValueError:
            raise ValueError(f"Paciente com ID {patient_id} não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao buscar paciente: {str(e)}")
        
    async def get_patient_by_cpf(self, cpf: str) -> Patient:
        try:
            patient = await self.repository.get_by_cpf(cpf)
            return patient
        except ValueError:
            raise ValueError(f"Paciente com CPF {cpf} não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao buscar paciente pelo CPF: {str(e)}")
        
    async def get_all_patients(self) -> list:
        try:
            patients = await self.repository.get_all()
            return patients
        except Exception as e:
            raise Exception(f"Erro ao listar pacientes: {str(e)}")
        
    async def update_patient(self, patient_id: int, name: str = None, cpf: str = None, birth_date: str = None,
                             medical_insurance: str = None, city: str = None, email: str = None, phone: str = None) -> Patient:
        try:
            updated_patient = await self.repository.update(patient_id, name, cpf, birth_date, medical_insurance, city, email, phone)
            return updated_patient
        except ValueError:
            raise ValueError(f"Paciente com ID {patient_id} não encontrado")
        except IntegrityError:
            raise ValueError(f"O CPF {cpf} ou email {email} já estão em uso")
        except Exception as e:
            raise Exception(f"Erro ao atualizar paciente: {str(e)}")
        
    async def delete_patient(self, patient_id: int) -> None:
        try:
            await self.repository.delete(patient_id)
        except ValueError:
            raise ValueError(f"Paciente com ID {patient_id} não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao deletar paciente: {str(e)}")
        
        