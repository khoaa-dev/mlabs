import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")

# Initialize database
db = SQLAlchemy()

