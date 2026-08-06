from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
import os

db_env = os.getenv("DATABASE_URL")

if db_env:
    DATABASE_URL = db_env
    if DATABASE_URL.startswith("sqlite"):
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False}
        )
    else:
        engine = create_engine(DATABASE_URL)
elif os.getenv("VERCEL"):
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
else:
    DATABASE_URL = "sqlite:///./sqlite.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    Base.metadata.create_all(bind=engine)
except Exception as err:
    print("Database initialization notice:", err)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
