<div align="center">
  <h1> FutureRole API: AI Job Search Platform</h1>
  
  <p>
    <b>A next-generation, agentic AI recruitment tool that bridges the gap between candidates and their perfect roles.</b>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
  </p>
</div>

---

##  Overview

**FutureRole** goes beyond standard keyword-matching. By utilizing **Groq's hyper-fast LLaMA-3.3-70b**, **LangChain multi-agent workflows**, and **In-Memory Vector Search**, this platform analyzes a candidate's resume holistically to retrieve, rank, and explain job matches in real-time.

---

## Core Features

| Feature | Description |
| :--- | :--- |
|  **Live Agent Reasoning** | Watch the AI "think" in real-time via Server-Sent Events (SSE). |
|  **Hybrid Scoring Engine** | Combines Semantic Similarity (40%), LLM Heuristics (30%), Rule-based Logic (20%), and Recency (10%). |
|  **Intelligent Resume Parsing** | Deep extraction of skills, experience level, and role alignment from PDFs. |
|  **Explainable AI (XAI)** | Plain-English explanations of skill gaps and alignment for every job. |
|  **Mock Interview Gen** | Automatically generates customized interview prep questions tailored perfectly to the match. |

---

##  Architecture Workflow

The backend is driven by a decentralized agent architecture:

1. **`PlannerAgent`**: Decides the exact pipeline of execution based on user payload.
2. **`JobSearchAgent`**: Interfaces with the SerpAPI for live remote/local job retrieval.
3. **`ResumeAgent`**: Extracts text from PDFs and categorizes technical parameters.
4. **`MatchingAgent`**: Cross-references embeddings and executes LLM-driven match scoring.
5. **`ExplanationAgent`**: Spins up parallel evaluation to generate actionable insights and interview questions.

---

##  Quick Start Guide

### 1. Repository Setup
```bash
git clone https://github.com/SantoshRM-1/AI-Job-Ajent.git
cd AI-Job-Ajent
```

### 2. Environment Variables
Create a `.env` file in the root configuration:
```env
SERP_API_KEY=your_serpapi_job_search_key
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### 3. Backend Initialization (FastAPI)
```bash
# Set up a clean virtual environment
python -m venv backend/venv
.\backend\venv\Scripts\activate   # (Windows)
# source backend/venv/bin/activate  (Mac/Linux)

# Install Dependencies
pip install -r backend/requirements.txt

# Boot the Server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Frontend Initialization (React 19)
Open a **secondary terminal**:
```bash
cd frontend
npm install
npm run dev
```

>  **You're all set!** Visit `http://localhost:5173`, upload your resume, and let the agents do the heavy lifting!

---

