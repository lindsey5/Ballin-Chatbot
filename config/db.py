from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import os

# Load environment variables
DB_USER = os.getenv("DB_USER", "sgroot")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "ballin_wear")

# SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(SQLALCHEMY_DATABASE_URL)

# Create engine with SSL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=180,
    connect_args={
        "ssl": {"ssl_ca": None, "check_hostname": True}  
    }
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Test connection
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("✅ Connected to MySQL successfully!")
except SQLAlchemyError as e:
    print("❌ Failed to connect to the database:", e)
