from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
import os

if os.getenv("VERCEL"):
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
