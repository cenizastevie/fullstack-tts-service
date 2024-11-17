from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ImageMetadata(Base):
    __tablename__ = "image_metadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    date = Column(Date)
    patient_id = Column(String)
    source_id = Column(String)
    diagnosis = Column(String)