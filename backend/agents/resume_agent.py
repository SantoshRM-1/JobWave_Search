import re
import uuid

from backend.services.pdf_parser import parse_pdf_from_bytes
from backend.services.stream_manager import stream_manager

SKILLS = ["Python", "Java", "JavaScript", "TypeScript", "React", "Next.js", "Node.js", "SQL", "PostgreSQL", "MongoDB", "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "CI/CD", "Terraform", "Linux", "REST APIs", "GraphQL", "Machine Learning", "Data Analysis", "Pandas", "NumPy", "TensorFlow", "PyTorch", "Power BI", "Tableau", "Figma", "HTML", "CSS", "Tailwind CSS", "FastAPI", "Django", "Flask"]

def local_resume_summary(text: str) -> dict:
    lower = text.lower()
    skills = [skill for skill in SKILLS if re.search(r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)", lower)]
    years = [int(year) for year in re.findall(r"(\d+)\+?\s*(?:years?|yrs?)", lower)]
    level = "Senior" if any(year >= 6 for year in years) else "Mid" if any(year >= 2 for year in years) else "Junior"
    role = re.search(r"(?:software|data|machine learning|frontend|backend|full stack|devops|product)\s+(?:engineer|developer|analyst|scientist|manager)", lower)
    return {"skills": skills[:30], "experience_level": level, "role_preference": role.group(0).title() if role else "Software Engineer"}

async def analyze_resume(file_bytes: bytes, session_id: str):
    await stream_manager.emit(session_id, "ACTION", "Reading your resume and extracting profile details.")
    text = parse_pdf_from_bytes(file_bytes)
    if not text.strip():
        await stream_manager.emit(session_id, "ERROR", "No selectable text was found in this PDF. Please upload a text-based resume PDF.")
        return None
    parsed_data = local_resume_summary(text)
    await stream_manager.emit(session_id, "DECISION", f"Resume profile ready: {len(parsed_data['skills'])} skills found.")
    return {"id": str(uuid.uuid4()), "raw_text": text, "parsed_data": parsed_data}
