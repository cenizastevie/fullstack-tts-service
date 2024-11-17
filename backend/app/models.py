from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ImageMetadata(Base):
    __tablename__ = "image_metadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), index=True)
    date = Column(Date)
    patient_id = Column(String(50))
    source_id = Column(String(50))
    diagnosis = Column(String(255))