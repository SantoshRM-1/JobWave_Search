from typing import Any, Dict, Optional

from backend.agents.explanation_agent import generate_explanations
from backend.agents.job_search_agent import run_search
from backend.agents.matching_agent import match_jobs
from backend.agents.resume_agent import analyze_resume
from backend.services.stream_manager import stream_manager


async def orchestrate_flow(query: str, location: str, session_id: str, resume_bytes: Optional[bytes] = None) -> Dict[str, Any]:
    """Run a reliable resume-first job search and matching workflow."""
    has_resume = bool(resume_bytes)
    await stream_manager.emit(session_id, "ACTION", "Starting your job search.")

    resume_data = None
    if has_resume:
        resume_data = await analyze_resume(resume_bytes, session_id)
        if not resume_data:
            await stream_manager.emit(session_id, "ERROR", "Could not read this resume. Please upload a text-based PDF.")

    # An uploaded resume can drive the search, but users may still override it.
    effective_query = query.strip()
    if not effective_query and resume_data:
        effective_query = resume_data["parsed_data"].get("role_preference", "")
    effective_query = effective_query or "Software Engineer"

    await stream_manager.emit(session_id, "THOUGHT", f"Searching broadly for {effective_query!r} roles.")
    jobs = await run_search(effective_query, location, session_id)

    if jobs and resume_data:
        jobs = await match_jobs(jobs, resume_data, location, session_id)
        jobs = await generate_explanations(jobs, resume_data, session_id)

    await stream_manager.emit(session_id, "ACTION", "Search complete. Your results are ready.")
    await stream_manager.close_stream(session_id)
    return {
        "session_id": session_id,
        "results": jobs,
        "resume": resume_data.get("parsed_data") if resume_data else None,
    }
