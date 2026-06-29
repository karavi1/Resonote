import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if os.getenv("FLASK_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()


def _build_database_url() -> str:
    # Preferred: a single Postgres connection string (e.g. from Neon).
    url = os.getenv("DATABASE_URL")
    if url:
        # SQLAlchemy needs the "postgresql://" scheme; Neon/Heroku style
        # "postgres://" URLs are normalized here.
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://"):]
        return url

    # Fallback: build from individual parts.
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    host = os.getenv("DATABASE_HOST")
    port = os.getenv("DATABASE_PORT", "5432")
    db_name = os.getenv("DATABASE_NAME")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}?sslmode=require"


DATABASE_URL = _build_database_url()
# pool_pre_ping avoids stale connections when Neon's serverless compute
# scales to zero and the first query reconnects.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)