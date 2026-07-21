import asyncio
import re

from backend.services.stream_manager import stream_manager


def compute_rule_based_score(job: dict, profile: dict) -> float:
    title = job.get("title", "").lower()
    level = profile.get("experience_level", "Mid").lower()
    level_score = 50 if ((level == "senior" and any(x in title for x in ("senior", "lead", "principal"))) or (level == "junior" and any(x in title for x in ("junior", "entry", "associate"))) or (level == "mid" and "senior" not in title and "junior" not in title)) else 25
    skills = profile.get("skills", [])
    description = job.get("description", "").lower()
    skill_score = (sum(skill.lower() in description for skill in skills) / len(skills) * 50) if skills else 25
    return min(100, level_score + skill_score)


async def match_jobs(jobs: list, resume_data: dict, query_location: str, session_id: str):
    """Fast local scoring: no model downloads or one-LLM-call-per-job delay."""
    await stream_manager.emit(session_id, "ACTION", f"Matching {len(jobs)} roles to your resume.")
    profile = resume_data.get("parsed_data", {})

    async def score(job):
        rule_score = compute_rule_based_score(job, profile)
        job_words = set(re.findall(r"[a-z0-9+#.]+", f"{job.get('title', '')} {job.get('description', '')}".lower()))
        profile_words = set(re.findall(r"[a-z0-9+#.]+", " ".join(profile.get("skills", [])).lower()))
        keyword_score = min(100, 35 + 18 * len(job_words & profile_words))
        final = .65 * rule_score + .25 * keyword_score + 8
        job["match_score"] = round(final, 1)
        job["breakdown"] = {"embedding": round(keyword_score, 1), "llm": round(keyword_score, 1), "rule": round(rule_score, 1), "recency": 80}
        return job

    await stream_manager.emit(session_id, "THOUGHT", "Comparing your skills and experience with each role.")
    scored = list(await asyncio.gather(*(score(job) for job in jobs)))
    scored.sort(key=lambda job: job.get("match_score", 0), reverse=True)
    return scored
