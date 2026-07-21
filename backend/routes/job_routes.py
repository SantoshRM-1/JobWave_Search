import uuid
from fastapi import APIRouter, Form, UploadFile, File, BackgroundTasks, Depends, HTTPException
from typing import Optional, Dict
from backend.agents.orchestrator import orchestrate_flow
from sqlalchemy.orm import Session
from backend.models.database import get_db
from backend.models.models import JobInteraction, Job
from backend.models.schemas import JobInteractionCreate
from backend.services.stream_manager import stream_manager

router = APIRouter()

# Temporary in-memory cache for results before persisting finalized jobs (since our orchestrator returns full job dicts)
# In production, the orchestrator should directly write finished jobs to the DB.
job_results_cache: Dict[str, dict] = {}


async def read_resume(resume: Optional[UploadFile]) -> Optional[bytes]:
    if not resume or not resume.filename:
        return None
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF resume.")
    contents = await resume.read()
    if not contents.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="That file is not a valid PDF.")
    if len(contents) > 8 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Please upload a PDF smaller than 8 MB.")
    return contents

async def run_orchestrator_background(query: str, location: str, resume_bytes: Optional[bytes], session_id: str):
    """Executes the AI orchestrator in the background and stores the result."""
    try:
        # Pass the session_id so all SSE events go to the correct client queue
        result = await orchestrate_flow(query, location, session_id, resume_bytes)
        # Store results temporarily
        job_results_cache[session_id] = {"jobs": result.get("results", []), "resume": result.get("resume")}
    except Exception as e:
        print(f"Background task failed: {e}")
        await stream_manager.emit(session_id, "ERROR", f"Agent execution failed: {str(e)}")
        await stream_manager.close_stream(session_id)

@router.post("/match-jobs")
async def match_jobs(
    background_tasks: BackgroundTasks,
    query: str = Form(...),
    location: Optional[str] = Form(default=""),
    resume: Optional[UploadFile] = File(None)
):
    """
    1. Generates a session_id.
    2. Sends the heavy lifting to a background task so we don't block.
    3. Returns the session_id so frontend can immediately subscribe to /agent-stream/{session_id}
    """
    session_id = str(uuid.uuid4())
    
    resume_bytes = await read_resume(resume)
        
    background_tasks.add_task(run_orchestrator_background, query, location, resume_bytes, session_id)
    
    return {"session_id": session_id, "message": "Agent execution started."}


@router.post("/search")
async def search_now(
    query: str = Form(default=""),
    location: Optional[str] = Form(default=""),
    resume: Optional[UploadFile] = File(None),
):
    """One reliable request for the web UI; ideal for serverless/Vercel hosting."""
    resume_bytes = await read_resume(resume)
    session_id = str(uuid.uuid4())
    result = await orchestrate_flow(query, location or "", session_id, resume_bytes)
    return {"jobs": result.get("results", []), "resume": result.get("resume")}

@router.get("/jobs/results/{session_id}")
async def get_match_results(session_id: str):
    """Polling endpoint or fetch once stream ends to get the compiled JSON results."""
    return job_results_cache.get(session_id, {"jobs": [], "resume": None})

@router.post("/jobs/interact")
async def log_job_interaction(interaction: JobInteractionCreate, db: Session = Depends(get_db)):
    """Log when a user views, saves, or clicks apply."""
    # Ensure job is present in db before logging
    # Note: we skip full db job insertion logic for brevity here, assuming jobs exist or are upserted when fetched
    new_interaction = JobInteraction(job_id=interaction.job_id, action=interaction.action)
    db.add(new_interaction)
    db.commit()
    return {"status": "success"}
    
@router.get("/jobs/saved")
async def get_saved_jobs(db: Session = Depends(get_db)):
    """Fetch jobs the user saved."""
    saved_interactions = db.query(JobInteraction).filter(JobInteraction.action == "saved").all()
    # Mocking return since real job table insert needs slightly more routing logic
    return {"saved_job_ids": [i.job_id for i in saved_interactions]}
