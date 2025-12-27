import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Construct Database URL from environment variables
# Format: postgresql://user:password@host:port/dbname
DATABASE_URL = "postgresql://{user}:{password}@{host}:{port}/{db}".format(
    user=os.getenv("POSTGRES_USER", "pharma_user"),
    password=os.getenv("POSTGRES_PASSWORD", "pharma_password"),
    host=os.getenv("POSTGRES_HOST", "db"), # 'db' matches the service name in docker-compose
    port=os.getenv("POSTGRES_PORT", "5432"),
    db=os.getenv("POSTGRES_DB", "pharma_chat_db"),
)

# 2. Create Database Engine
# This represents the core interface to the database
engine = create_engine(DATABASE_URL)

# 3. Create SessionLocal class
# Each instance of this class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class for models
# All database models (tables) will inherit from this class
Base = declarative_base()

# 5. Dependency injection utility
# Used in FastAPI endpoints to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()