from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import os

# Optionally, load from environment variables for security
DB_USER = os.getenv("DB_USER", "sgroot")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "ballin_wear")

# SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))  # wrap the string in text()
        print("✅ Connected to MySQL in XAMPP successfully!")
except SQLAlchemyError as e:
    print("❌ Failed to connect to the database:", e)

from models.Product import Product
from models.Variant import Variant
from models.Thumbnail import Thumbnail

Base.metadata.create_all(bind=engine)