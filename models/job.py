#!/usr/bin/env python3
""" holds class Jobs"""

import sqlalchemy
from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP, Date, ForeignKey
from sqlalchemy.orm import relationship
from base import Base
from sqlalchemy.sql import func

class Job(Base):
    """Represents of Job."""

    __tablename__ = 'Jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    employer_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    salary = Column(String(50))
    location = Column(String(100), nullable=False)
    job_type = Column(Enum('full-time', 'part-time', 'contract', name='job_type_enum', nullable=False))
    application_deadline = Column(Date)
    skills_required = Column(Text, nullable=False)
    preferred_qualifications = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    employer = relationship('models.user.User', back_populates='jobs')

    def to_dict(self):
        """Converts the Job instance to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "requirements": self.requirements,
            "employer_id": self.employer_id,
            "salary": self.salary,
            "location": self.location,
            "job_type": self.job_type,
            "application_deadline": str(self.application_deadline),
            "skills_required": self.skills_required,
            "preferred_qualifications": self.preferred_qualifications,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
