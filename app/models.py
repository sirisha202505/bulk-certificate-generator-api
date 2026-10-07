from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from .database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending", nullable=False)
    total = Column(Integer, default=0, nullable=False)
    successful = Column(Integer, default=0, nullable=False)
    failed = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, nullable=False)
    recipient_name = Column(String, nullable=False)
    recipient_email = Column(String, nullable=False)
    course_name = Column(String, nullable=False)
    certificate_path = Column(Text, nullable=True)
    status = Column(String, default="pending", nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)