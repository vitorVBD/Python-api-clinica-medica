import re
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import validates
from database.database import db as Base

class Patient(Base):
    __tablename__ = 'pacientes'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    birth_date = Column(Date, nullable=False)
    medical_insurance = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(15), nullable=False, unique=True)
    created_at = Column(Date, default=datetime.timezone.utc)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Nome obrigatório")
        return name
    
    @validates('cpf')
    def validate_cpf(self, key, cpf):
        if not cpf:
            raise ValueError("CPF obrigatório")
        pattern = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
        if not pattern.match(cpf):
            raise ValueError("CPF inválido, digite no formato xxx.xxx.xxx-xx")
        return cpf

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


    @validates('city')
    def validate_city(self, key, city):
        if not city:
            raise ValueError("Cidade obrigatória")
        return city

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            return None
        pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not pattern.match(email):
            raise ValueError("Email inválido")
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        if not phone:
            raise ValueError("Telefone obrigatório")
        pattern = re.compile(r'^\(\d{2}\) \d{5}-\d{4}$')
        if not pattern.match(phone):
            raise ValueError("Número de telefone inválido, digite no formato (xx) xxxxx-xxxx")
        return phone    