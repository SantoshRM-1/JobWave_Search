<div align="center">

  <h1>🌊 JobWave Search</h1>
  <p><b>An Agentic AI-Powered Job Discovery & Match Ranking Engine</b></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/React_19-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React 19" />
    <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
    <img src="https://img.shields.io/badge/Groq_LLaMA_3.3_70B-F34B21?style=for-the-badge&logo=groq&logoColor=white" alt="Groq" />
    <img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel" />
  </p>

</div>

---

## 📌 Overview

**JobWave Search** (formerly *AI Job Agent*) is an intelligent, multi-agent recruitment platform designed to connect job seekers with tailored career opportunities. Unlike conventional search engines that rely purely on basic keyword matching, JobWave Search utilizes **Groq-powered LLaMA 3.3 (70B)**, a multi-agent orchestration pipeline, and automated PDF resume analysis to match, rank, and explain job fit in real time.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 📄 **Smart PDF Resume Parsing** | Extracts skills, target roles, and experience levels directly from uploaded PDF resumes using PyMuPDF and LLaMA 3.3. |
| 🤖 **Multi-Agent Orchestration** | Autonomous agent workflow featuring specialized Planner, Search, Resume, Matching, and Explanation agents. |
| ⚡ **Live Real-Time SSE Streaming** | Streams agent reasoning steps and thinking status via Server-Sent Events (SSE) directly to the user interface. |
| 🎯 **AI Fit Scoring & XAI** | Generates percentage match scores, plain-English explanations of fit, and skill gap analyses. |
| 💡 **Tailored Interview Question Generator** | Automatically crafts custom interview prep questions tailored specifically to each candidate and role. |
| 🔍 **Multi-Provider Job Aggregation** | Fetches live jobs from **JSearch API (RapidAPI)** and **Google Jobs (SerpApi)** with fallback mechanisms. |
| 🎨 **Modern Futuristic UI** | Built with React 19, Framer Motion, and Tailwind CSS v4 featuring dark mode aesthetics and glassmorphism. |
| 🚀 **Vercel Serverless Ready** | Pre-configured with unified frontend build and backend serverless API handlers for instant deployment. |

---

## 🏗️ System Architecture

```mermaid
graph TD
    Client[React 19 Frontend UI] -->|POST /api/search or SSE /agent-stream| API[FastAPI Server / Vercel API]
    
    subgraph Multi-Agent Orchestrator
        API --> Orchestrator[Orchestrator]
        Orchestrator --> Planner[Planner Agent]
        Orchestrator --> ResumeAgent[Resume Agent]
        Orchestrator --> SearchAgent[Job Search Agent]
        Orchestrator --> MatchAgent[Matching Agent]
        Orchestrator --> ExplainAgent[Explanation Agent]
    end

    ResumeAgent -->|PDF Parsing| PyMuPDF[PyMuPDF + Groq LLaMA 3.3]
    SearchAgent -->|Live Job Search| JSearch[JSearch RapidAPI / SerpApi Google Jobs]
    MatchAgent -->|Scoring Engine| Scoring[Hybrid Keyword + LLM Matcher]
    ExplainAgent -->|AI Insights & Questions| Groq[Groq LLaMA 3.3 70B]
    
    Orchestrator -->|Real-Time Status| SSE[Server-Sent Events]
    SSE --> Client
```

---

## 🛠️ Technology Stack

### **Backend**
- **Framework**: Python 3.10+, FastAPI, Uvicorn
- **AI / LLM Engine**: Groq API (`llama-3.3-70b-versatile`)
- **PDF Parser**: PyMuPDF (`fitz`)
- **Database & ORM**: SQLite, SQLAlchemy
- **Data Validation**: Pydantic v2
- **External APIs**: RapidAPI (JSearch), SerpApi (Google Jobs)

### **Frontend**
- **Framework**: React 19 (Vite 8)
- **Styling**: Tailwind CSS v4, Framer Motion (Animations), Lucide React (Icons)
- **HTTP Client**: Native Fetch API / Axios

---

## 📂 Project Structure

```
JobWave_Search/
├── api/
│   └── index.py               # Vercel Serverless Function entrypoint
├── backend/
│   ├── agents/                # Multi-Agent implementation
│   │   ├── explanation_agent.py
│   │   ├── job_search_agent.py
│   │   ├── matching_agent.py
│   │   ├── orchestrator.py
│   │   ├── planner_agent.py
│   │   └── resume_agent.py
│   ├── models/                # SQLAlchemy & Pydantic models
│   ├── routes/                # FastAPI endpoints (job_routes, stream_routes)
│   ├── services/              # SSE Stream Manager
│   ├── tools/                 # JSearch API, SerpApi & Resume Analyzer tools
│   └── main.py                # FastAPI main application
├── frontend/
│   ├── src/
│   │   ├── components/        # React components (JobCard, SearchBar, etc.)
│   │   └── App.jsx            # Main dashboard application
│   ├── package.json           # Frontend dependencies
│   └── vite.config.js         # Vite configuration
├── package.json               # Root monorepo script configuration
├── requirements.txt           # Python backend dependencies
└── vercel.json                # Vercel deployment & route rewriting config
```

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/SantoshRM-1/JobWave_Search.git
cd JobWave_Search
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```env
# AI Models Key
GROQ_API_KEY=gsk_your_groq_api_key_here

# Job Search APIs (Choose either or both)
SERP_API_KEY=your_serpapi_key_here
RAPIDAPI_KEY=your_rapidapi_key_here
```

### 3. Start Backend Server
```bash
# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn backend.main:app --reload --port 8000
```

### 4. Start Frontend Client
In a new terminal tab:
```bash
cd frontend
npm install
npm run dev
```

Open your browser at `http://localhost:5173`.

---

## ☁️ Deployment on Vercel

This repository is optimized for one-click deployment on **Vercel**.

1. Import your GitHub repository (`SantoshRM-1/JobWave_Search`) into **Vercel**.
2. Set **Root Directory** to `.` (leave default root).
3. Add your Environment Variables (`GROQ_API_KEY`, `SERP_API_KEY`, etc.) in Vercel Project Settings.
4. Deploy! Vercel will automatically build the React frontend and deploy the FastAPI backend as serverless functions.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
