#!/usr/bin/python3
"""Creating the database engine."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import declarative_base
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

"""Determine the port or set a default port if not provided."""
db_port = int(DB_PORT) if DB_PORT is not None else 3306

"""Database URL."""
mysql_db_url = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

"""Create database engine with connection pool settings."""
engine = create_engine(
    mysql_db_url,
    pool_size=20,         # Increase pool size
    max_overflow=10,      # Increase overflow limit
    pool_timeout=30,      # Increase timeout (optional)
    pool_recycle=3600     # Recycle connections every hour (optional)
)

try:
    conn = engine.connect()
    print('db.connected')
    print('Connection object is :{}'.format(conn))
except Exception as e:
    print('db not connected:', e)

"""Create a scope_session factory."""
SessionLocal = scoped_session(sessionmaker(bind=engine))

"""Base class for declarative ORM models."""
Base = declarative_base()

"""Function to create all tables."""
def create_all_tables():
    Base.metadata.create_all(bind=engine)

"""Function to drop all tables."""
def drop_all_tables():
    Base.metadata.drop_all(bind=engine)
