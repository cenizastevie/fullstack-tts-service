from sqlalchemy import Column, String, Date, Integer, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ImageMetadata(Base):
    __tablename__ = "image_metadata"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), index=True)
    date = Column(Date)
    patient_id = Column(String(50))
    source_id = Column(String(50))
    diagnosis = Column(String(255))

    __table_args__ = (
        UniqueConstraint('file_name', 'date', 'patient_id', 'source_id', 'diagnosis', name='_image_metadata_uc'),
    )