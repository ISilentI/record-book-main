import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Record(Base):
    __tablename__ = "record"
    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    student_guid = Column(UUID(as_uuid=True), ForeignKey("student.guid"))
    student = relationship("Student", back_populates="records", lazy="joined", uselist=False)
    teacher_guid = Column(UUID(as_uuid=True), ForeignKey("teacher.guid"))
    teacher = relationship("Teacher", back_populates="records", lazy="joined", uselist=False)
    name = Column(String, nullable=False)
    term = Column(Integer, nullable=False)
    year_guid = Column(UUID(as_uuid=True), ForeignKey("year.guid"))
    year = relationship("Year", backref="years", lazy="joined", uselist=False)
    mark = Column(String, nullable=False)
    exam_date = Column(DateTime(timezone=True), nullable=False)
    exam_type = Column(String, nullable=False)
