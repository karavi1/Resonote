import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Build the DATABASE_URL from parts
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
port = os.getenv("DATABASE_PORT", "3306")
db_name = os.getenv("DATABASE_NAME")

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)