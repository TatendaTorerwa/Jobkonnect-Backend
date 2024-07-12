#!/usr/bin/env python3
""" holds class Applications"""

import sqlalchemy
from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP, Date, ForeignKey
from sqlalchemy.orm import relationship
from base import Base
from models.user import User
from models.job import Job
from sqlalchemy.sql import func

class Application(Base):
    """Represents of Application."""

    __tablename__ = 'Applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey('Jobs.id'), nullable=False)
    employer_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    resume = Column(String(255))
    cover_letter = Column(String(255))
    status = Column(Enum('submitted', 'under_review', 'rejected', 'accepted', name='status_enum'), default='submitted')
    submitted_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    years_of_experience = Column(Integer, nullable=True)

    job = relationship('Job', back_populates='applications')
    user = relationship('User', foreign_keys=[user_id], back_populates='applications')
    employer = relationship('User', foreign_keys=[employer_id])

    def to_dict(self):
        """Converts the Application instance to a dictionary."""
        return {
            "id": self.id,
            "job_id": self.job_id,
            "user_id": self.user_id,
            "resume": self.resume,
            "cover_letter": self.cover_letter,
            "status": self.status,
            "submitted_at": self.submitted_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "years_of_experience": self.years_of_experience
        }
