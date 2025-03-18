import re
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import validates
from database.database import db as Base

class Secretary(Base):
    __tablename__ = 'secretarias'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Nome obrigatório")
        return name
    
    @validates('birth_date')
    def validate_birth_date(self, key, birth_date):
        if not birth_date:
            raise ValueError("Data de nascimento obrigatória")
        
        if isinstance(birth_date, str):
            try:
                birth_date = datetime.strptime(birth_date, '%d-%m-%Y').date()
            except ValueError:
                raise ValueError("Data de nascimento inválida, verifique o formato e a validade")
        
        return birth_date
    
    @validates('phone')
    def validate_phone(self, key, phone):
        if not phone:
            raise ValueError("Telefone obrigatório")
        pattern = re.compile(r'^\(\d{2}\)\s\d{5}-\d{4}$')
        if not pattern.match(phone):
            raise ValueError("Telefone inválido, digite no formato (xx) xxxxx-xxxx")
        return phone
    
    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email obrigatório")
        pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not pattern.match(email):
            raise ValueError("Email inválido, digite um email válido")
        return email
    
    @validates('password')
    def validate_hashed_password(self, key, password):
        if not password:
            raise ValueError("Senha obrigatória")
        return password