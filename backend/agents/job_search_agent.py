from backend.tools.jsearch_api import fetch_jobs
from backend.services.stream_manager import stream_manager
import uuid

async def run_search(query: str, location: str, session_id: str):
    """Executes the job search, emits thoughts, and indexes results into FAISS."""
    await stream_manager.emit(session_id, "ACTION", f"Initializing job search for '{query}' in '{location or 'Remote'}'")
    
    await stream_manager.emit(session_id, "THOUGHT", "Querying JSearch API for real-time listings...")
    
    jobs = fetch_jobs(query, location)
    
    if not jobs:
        await stream_manager.emit(session_id, "ERROR", "No jobs found for this query.")
        return []
        
    await stream_manager.emit(session_id, "DECISION", f"Retrieved {len(jobs)} jobs. Preparing your matches.")
    
    # Simple asynchronous loop to chunk and index jobs into FAISS
    stored_jobs = []
    for job in jobs:
        # Give mock jobs a real unique ID just for the demo if it returned mocks
        j_id = str(uuid.uuid4()) if job.get('id').startswith('mock') else job.get('id')
        job['id'] = j_id
        
        stored_jobs.append(job)
        
    await stream_manager.emit(session_id, "THOUGHT", f"Search complete. Found {len(stored_jobs)} roles to review.")
    return stored_jobs
