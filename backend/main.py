import sqlite3
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from database import DB_PATH
from graph_engine import NexusGraphEngine
from ai_agent import GeminiEnterpriseAgent

app = FastAPI(
    title="NexusGraph AI — Enterprise Process x Role x Skill Intelligence Engine",
    description="Combined Assignment 11 & Assignment 4 Implementation for Modus Enterprise AI Challenge",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph_engine = NexusGraphEngine()
ai_agent = GeminiEnterpriseAgent()

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "system": "NexusGraph AI Engine",
        "assignments": ["Assignment 11", "Assignment 4"],
        "database": "Connected & Persisted (SQLite)",
        "model": "gemini-3.1-flash-lite",
        "api_key_status": "Secured via Environment (.env)"
    }

@app.get("/api/graph")
def get_graph():
    graph_engine.reload_graph()
    return graph_engine.get_cytoscape_elements()

@app.get("/api/roles")
def get_roles():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department, seniority FROM roles ORDER BY name ASC")
    roles = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return roles

@app.get("/api/skills")
def get_skills():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, trend FROM skills ORDER BY name ASC")
    skills = [dict(s) for s in cursor.fetchall()]
    conn.close()
    return skills

@app.get("/api/role/{role_id}/impact")
def get_role_impact(role_id: str):
    data = graph_engine.get_role_intelligence(role_id)
    if not data:
        raise HTTPException(status_code=404, detail="Role not found")
    return data

@app.get("/api/skill/{skill_id}/roles")
def get_roles_by_skill(skill_id: str):
    roles = graph_engine.get_roles_by_skill(skill_id)
    return {"skill_id": skill_id, "count": len(roles), "roles": roles}

@app.get("/api/process/{process_id}/roles")
def get_roles_by_process(process_id: str):
    roles = graph_engine.get_roles_by_process(process_id)
    return {"process_id": process_id, "count": len(roles), "roles": roles}

@app.get("/api/processes")
def get_processes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, business_purpose, automation_potential FROM processes")
    procs = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return procs

@app.post("/api/simulate-impact")
def simulate_impact(payload: dict = Body(...)):
    activity_id = payload.get("activity_id")
    if not activity_id:
        raise HTTPException(status_code=400, detail="activity_id is required")

    result = graph_engine.simulate_cascading_impact(activity_id)
    return result

@app.post("/api/ingest-surprise-record")
def ingest_surprise_record(payload: dict = Body(...)):
    record_type = payload.get("record_type", "Process")
    name = payload.get("name")
    context = payload.get("context", "")

    if not name:
        raise HTTPException(status_code=400, detail="Name is required for surprise record")

    ingested_data = ai_agent.process_surprise_record(record_type, name, context)
    graph_engine.reload_graph()

    return {
        "status": "success",
        "message": f"Successfully ingested {record_type} '{name}' and persisted to SQLite",
        "data": ingested_data,
        "updated_graph": graph_engine.get_cytoscape_elements()
    }

# Mount Frontend
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
FRONTEND_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def read_root():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "NexusGraph AI Backend API Online"}

if __name__ == "__main__":
    import uvicorn
    from config import PORT, HOST
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
