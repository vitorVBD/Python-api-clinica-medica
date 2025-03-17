import re
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates
from database.database import db as Base
import validators

class Doctor(Base):
    __tablename__ = 'medicos'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    specialty = Column(String(100), nullable=True)
    phone = Column(String(15), nullable=False, unique=True)
    crm = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.timezone.utc)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Nome obrigatório")
        return name

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email obrigatório")
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise ValueError("Email inválido")
        return email

    @validates('password')
    def validate_password(self, key, password):
        if not password:
            raise ValueError("Senha obrigatória")
        return password

    @validates('phone')
    def validate_phone(self, key, phone):
        if not phone:
            raise ValueError("Telefone obrigatório")
        pattern = re.compile(r'^\(\d{2}\) \d{5}-\d{4}$')
        if not pattern.match(phone):
            raise ValueError("Número de telefone inválido, digite no formato (xx) xxxxx-xxxx")
        return phone

    @validates('crm')
    def validate_crm(self, key, crm):
        if not crm:
            raise ValueError("CRM obrigatório")
        pattern = re.compile(r'^\d{5,10}-[A-Z]{2}$')
        if not pattern.match(crm):
            raise ValueError("CRM inválido, digite no formato 99999-UF")
        
        uf = crm[-2:]
        ufs_validos = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
                       'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
                       'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
        if uf not in ufs_validos:
            raise ValueError("UF inválido no CRM")
        
        return crm