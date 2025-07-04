from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from vetclinic_api.core.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    __table_args__ = (
        # Blokada: jeden lekarz nie może mieć dwóch wizyt w tej samej sekundzie
        UniqueConstraint('doctor_id', 'visit_datetime', name='uq_doctor_visit_datetime'),
    )

    id             = Column(Integer, primary_key=True, index=True)
    doctor_id      = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    animal_id      = Column(Integer, ForeignKey("animals.id"), nullable=False)
    owner_id       = Column(Integer, ForeignKey("clients.id"), nullable=False)
    facility_id    = Column(Integer, ForeignKey("facilities.id"), nullable=False)
    visit_datetime = Column(DateTime, nullable=False)
    reason         = Column(Text,   nullable=True, comment="Powód wizyty lub rodzaj usługi")
    treatment      = Column(Text,   nullable=True, comment="Zastosowane leczenie podczas wizyty")
    priority       = Column(String, nullable=False, default="normalna", comment="Priorytet wizyty: normalna,pilna,nagła")
    weight         = Column(Float,  nullable=True, comment="Waga zwierzęcia podczas wizyty")
    notes          = Column(Text,   nullable=True, comment="Dodatkowe uwagi")
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
    updated_at     = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    fee            = Column(Float, nullable=True, default=0.0)
    tx_hash        = Column(String, nullable=True, comment="Hash transakcji on‐chain")

    doctor          = relationship("Doctor", back_populates="appointments")
    animal          = relationship("Animal", back_populates="appointments")
    owner           = relationship("Client", back_populates="appointments")
    medical_records = relationship("MedicalRecord", back_populates="appointment",cascade="all, delete-orphan",)
    facility        = relationship("Facility", back_populates="appointments")