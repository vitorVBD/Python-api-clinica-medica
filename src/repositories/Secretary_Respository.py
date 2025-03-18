from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from models.Secretary import Secretary
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

class Secretary_Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, birth_date: str, hashed_password: str, phone: str, email: str) -> Secretary:
        secretary = Secretary(
            name=name,
            birth_date=birth_date,
            hashed_password=hashed_password,
            phone=phone,
            email=email
        )

        try:
            self.session.add(secretary)
            await self.session.commit()
            await self.session.refresh(secretary)
            return secretary
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(f"O email {email} ou telefone {phone} já estão em uso")
        except Exception as e:
            await self.session.rollback()
            raise e
        

    async def get_by_id(self, secretary_id: int) -> Secretary:
        result = await self.session.execute(select(Secretary).filter(Secretary.id == secretary_id))
        secretary = result.scalars().first()
        if not secretary:
            raise ValueError(f"Secretária com ID {secretary_id} não encontrada")
        return secretary
    
    async def get_by_email(self, email: str) -> Secretary:
        result = await self.session.execute(select(Secretary).filter(Secretary.email == email))
        secretary = result.scalars().first()
        if not secretary:
            raise ValueError(f"Secretária com email {email} não encontrada")
        return secretary
    
    async def get_all(self) -> list:
        result = await self.session.execute(select(Secretary))
        secretaries = result.scalars().all()
        return await secretaries
    
    async def update(self, secretary_id: int, name: str = None, birth_date: str = None, hashed_password: str = None, phone: str = None, email: str = None) -> Secretary:
        secretary = await self.get_by_id(secretary_id)

        if name:
            secretary.name = name
        if birth_date:
            secretary.birth_date = birth_date
        if hashed_password:
            secretary.hashed_password = hashed_password
        if phone:
            secretary.phone = phone
        if email:
            secretary.email = email

        try:
            await self.session.commit()
            await self.session.refresh(secretary)
            return secretary
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(f"O email {email} ou telefone {phone} já estão em uso")
        except Exception as e:
            await self.session.rollback()
            raise e
        
    async def delete(self, secretary_id: int) -> None:
        secretary = await self.get_by_id(secretary_id)
        self.session.delete(secretary)
        await self.session.commit()
        return None