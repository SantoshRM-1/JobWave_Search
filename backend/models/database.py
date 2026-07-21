from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Vercel's deployed source directory is read-only. Saved jobs live in browser
# storage, while this temporary database keeps legacy interaction routes safe.
DATABASE_URL = "sqlite:////tmp/sqlite.db" if os.getenv("VERCEL") else "sqlite:///./sqlite.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
