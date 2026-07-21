import requests
import os
import re
from urllib.parse import quote_plus
from typing import List, Dict, Any

DEFAULT_PAGE_COUNT = 3
MAX_RESULTS = 30

def fetch_jobs(query: str, location: str = "") -> List[Dict[str, Any]]:
    """
    Fetches real job listings using the JSearch API (RapidAPI).
    Uses a default location if empty.
    """
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key or api_key == "your_rapidapi_key_here":
        print("Warning: RAPIDAPI_KEY not configured. Returning mock data.")
        return get_mock_jobs(query, location)

    # Defaults handling
    actual_location = location.strip() if location else "Remote"
    search_query = f"{query} {actual_location}"

    url = "https://jsearch.p.rapidapi.com/search"
    # Fetch a useful set; the old one-page request commonly returned just two jobs.
    querystring = {"query": search_query, "num_pages": str(DEFAULT_PAGE_COUNT)}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        data = response.json()
        jobs_raw = data.get("data", [])[:MAX_RESULTS]
        
        # Clean up data for the DB schema
        cleaned_jobs = []
        for job in jobs_raw:
            cleaned_jobs.append({
                "id": job.get("job_id"),
                "title": job.get("job_title"),
                "company": job.get("employer_name"),
                "location": ", ".join(filter(None, [job.get("job_city"), job.get("job_state"), job.get("job_country")])) or ("Remote" if job.get("job_is_remote") else actual_location),
                "description": job.get("job_description", "")[:3000],
                "apply_url": job.get("job_apply_link") or job.get("job_google_link"),
                "posted_at": job.get("job_posted_at_datetime_utc") or job.get("job_posted_at"),
                "employment_type": job.get("job_employment_type"),
            })
        return cleaned_jobs
    except Exception as e:
        print(f"JSearch API error: {e}")
        return get_mock_jobs(query, location)

def get_mock_jobs(query: str, location: str) -> List[Dict[str, Any]]:
    """Useful offline fallback: enough varied listings to test matching and pagination."""
    clean_query = re.sub(r"\s+", " ", query).strip() or "Software Engineer"
    companies = ["Northstar Labs", "Aster Cloud", "Orbit Systems", "PixelWorks", "Sage Data", "Vertex Labs", "Bluehaven", "Craftline", "Nexa", "Brightloop", "Kiteworks", "Helio"]
    levels = ["Associate", "Junior", "", "", "Senior", "Lead", "Principal", "", "Senior", "", "", ""]
    skills = ["Python, SQL and APIs", "React, TypeScript and testing", "AWS, Docker and CI/CD", "data analysis and dashboards"]
    return [
        {"id": f"mock_{i + 1}", "title": f"{level + ' ' if level else ''}{clean_query}", "company": company, "location": location or ("Remote" if i % 2 == 0 else "Bengaluru, India"), "description": f"Join {company} as a {clean_query}. Build reliable customer-facing products with {skills[i % len(skills)]}, communication, and problem solving.", "apply_url": f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(clean_query + ' ' + company)}", "employment_type": "Full-time"}
        for i, (company, level) in enumerate(zip(companies, levels))
    ]
