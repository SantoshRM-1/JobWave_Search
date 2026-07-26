"""
Planner Agent - Uses LangChain + Groq to plan execution steps.
Imports are lazy to prevent crashes when packages are not installed.
"""
from typing import List


def get_llm():
    from langchain_groq import ChatGroq
    from backend.config import GROQ_API_KEY, GROQ_MODEL
    return ChatGroq(model=GROQ_MODEL, temperature=0, api_key=GROQ_API_KEY)


async def create_plan(query: str, has_resume: bool) -> List[str]:
    """Generates a dynamic execution plan based on the inputs."""
    import json
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are the orchestration planner for an AI Job Search Agent.
        Your job is to read the user request and available data (e.g., if a resume exists) and map out the exact list of agentic steps needed.
        Valid steps:
        - "search_jobs"
        - "analyze_resume"
        - "match_jobs"
        - "rank_jobs"
        - "generate_explanations"
        
        Strictly output ONLY a valid JSON array of these string step actions, e.g. ["search_jobs", "analyze_resume"]. Do not include markdown blocks."""),
        ("user", "User query: {query}. Has uploaded resume: {has_resume}")
    ])

    llm = get_llm()
    chain = prompt | llm

    try:
        response = await chain.ainvoke({"query": query, "has_resume": str(has_resume)})
        clean_text = response.content.strip().strip('`').replace('json\n', '').replace('json', '')
        steps = json.loads(clean_text)
        return steps
    except Exception as e:
        print(f"PlannerAgent error: {e}")
        if has_resume:
            return ["search_jobs", "analyze_resume", "match_jobs", "generate_explanations"]
        else:
            return ["search_jobs"]
