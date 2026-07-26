from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Explicitly load from backend directory or project root
load_dotenv(dotenv_path="backend/.env")
load_dotenv(dotenv_path=".env")

from backend.models.database import engine, Base
from backend.routes.job_routes import router as job_router
from backend.routes.stream_routes import router as stream_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print("Lifespan DB notice:", e)
    yield

app = FastAPI(
    title="AI Job Search Agent",
    description="Multi-agent AI system for job matching & ranking",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_router)
app.include_router(stream_router)
app.include_router(job_router, prefix="/api")
app.include_router(stream_router, prefix="/api")

@app.get("/")
@app.get("/health")
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "AI Job Agent Running 🚀"}
