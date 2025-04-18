"""
Definicje modeli SQLAlchemy odpowiadających tabelom w bazie danych.
"""

from sqlalchemy import Column, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    totp_secret = Column(String, nullable=True, default=None)
    totp_confirmed = Column(Boolean, default=False)

    animals = relationship("Animal", back_populates="owner")
    appointments = relationship("Appointment", back_populates="owner")


    @property
    def role(self):
        return "klient"

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    permit_number = Column(String, nullable=False)
    totp_secret = Column(String, nullable=True, default=None)
    totp_confirmed = Column(Boolean, default=False)

    appointments = relationship("Appointment", back_populates="doctor")
    

    @property
    def role(self):
        return "lekarz"

class Consultant(Base):
    __tablename__ = "consultants"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    totp_secret = Column(String, nullable=True, default=None)
    totp_confirmed = Column(Boolean, default=False)
    
    @property
    def role(self):
        return "konsultant"
