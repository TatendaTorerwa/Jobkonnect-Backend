#!/usr/bin/env python3
"""Creating the database engine and tables."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base, engine
from models.user import User
from models.job import Job
from models.application import Application

""" Create a session factory."""
Session = sessionmaker(bind=engine)

def create_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    """If this script is run directly, create all tables in the database."""
    create_tables()
    print("Tables created successfully.")
