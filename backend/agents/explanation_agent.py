import asyncio
from typing import Any, Dict, List

from backend.services.stream_manager import stream_manager


async def generate_explanation(job: Dict[str, Any], resume_data: Dict[str, Any]) -> Dict[str, Any]:
    profile = resume_data.get("parsed_data", {})
    skills = profile.get("skills", [])
    description = str(job.get("description", "")).lower()
    matched = [skill for skill in skills if skill.lower() in description][:6]
    gaps = [skill for skill in ("Cloud", "Testing", "Communication") if skill.lower() not in description]
    score = job.get("match_score", 0)
    confidence = "High confidence" if score >= 75 else "Moderate fit" if score >= 55 else "Exploratory match"
    focus = ", ".join(matched[:3]) or "your overall experience"
    return {"reasoning": f"This role matches {focus} and your {profile.get('experience_level', 'current')} experience level. Open the job link to confirm the requirements and apply.", "matched_skills": matched, "missing_skills": gaps, "interview_questions": [], "confidence": confidence}


async def generate_explanations(jobs: List[Dict[str, Any]], resume_data: Dict[str, Any], session_id: str):
    await stream_manager.emit(session_id, "ACTION", "Creating clear match reasons for the top roles.")
    await stream_manager.emit(session_id, "THOUGHT", "Highlighting the skills that make each role relevant.")
    top = list(await asyncio.gather(*(generate_explanation(job, resume_data) for job in jobs[:10])))
    for index, explanation in enumerate(top):
        jobs[index].update(explanation)
    return jobs
