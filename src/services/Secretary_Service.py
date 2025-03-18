from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from repositories import Secretary_Respository
from repositories.Secretary_Respository import Secretary
from sqlalchemy.exc import IntegrityError

class Secretary_Service:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = Secretary_Respository(session)

    async def create_secretary(self, name: str, birth_date: str, hashed_password: str, phone: str, email: str) -> Secretary:
        try:
            secretary = await self.repository.create(name, birth_date, hashed_password, phone, email)
            return secretary
        except IntegrityError:
            raise ValueError(f"Email {email} ou telefone {phone} já estão em uso")
        except Exception as e:
            raise Exception(f"Erro ao criar secretário: {str(e)}")
    
    async def get_secretary_by_id(self, secretary_id: int) -> Secretary:
        try:
            secretary = await self.repository.get_by_id(secretary_id)
            return secretary
        except ValueError:
            raise ValueError(f"Secretário com ID {secretary_id} não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao buscar secretário: {str(e)}")
    
    async def get_secretary_by_email(self, email: str) -> Secretary:
        try:
            secretary = await self.repository.get_by_email(email)
            return secretary
        except ValueError:
            raise ValueError(f"Secretário com email {email} não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao buscar secretário pelo email: {str(e)}")
    
    async def get_all_secretaries(self) -> list:
        try:
            secretaries = await self.repository.get_all()
            return secretaries
        except Exception as e:
            raise Exception(f"Erro ao listar secretários: {str(e)}")
    
    async def update_secretary(self, secretary_id: int, name: str = None, birth_date: str = None, hashed_password: str = None, phone: str = None, email: str = None) -> Secretary:
        try:
            updated_secretary = await self.repository.update(secretary_id, name, birth_date, hashed_password, phone, email)
            return updated_secretary
        except ValueError:
            raise ValueError(f"Secretário com ID {secretary_id} não encontrado")
        except IntegrityError:
            raise ValueError(f"O email {email} ou telefone {phone} já estão em uso")
        except Exception as e:
            raise Exception(f"Erro ao atualizar secretário: {str(e)}")
    
    async def delete_secretary(self, secretary_id: int) -> None:
        try:
            await self.repository.delete(secretary_id)
        except ValueError:
            raise ValueError(f"Secretário com ID {secretary_id} não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao deletar secretário: {str(e)}")