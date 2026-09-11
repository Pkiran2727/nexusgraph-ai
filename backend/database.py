import os
import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "nexus_intelligence.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS value_chains (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        industry TEXT NOT NULL,
        description TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processes (
        id TEXT PRIMARY KEY,
        value_chain_id TEXT,
        name TEXT NOT NULL,
        business_purpose TEXT,
        automation_potential TEXT, -- Low, Medium, High
        human_involvement TEXT,
        FOREIGN KEY(value_chain_id) REFERENCES value_chains(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id TEXT PRIMARY KEY,
        process_id TEXT,
        name TEXT NOT NULL,
        execution_mode TEXT, -- Manual, Hybrid, Automated
        ai_exposure TEXT, -- Low, Medium, High
        FOREIGN KEY(process_id) REFERENCES processes(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roles (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT,
        seniority TEXT,
        future_risk_score REAL, -- 0.0 to 1.0
        summary TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT, -- Technical, Operational, Strategic, Soft
        trend TEXT -- Emerging, Increasing, AI-Augmented, Declining, Enduring
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS graph_edges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id TEXT NOT NULL,
        source_type TEXT NOT NULL, -- Process, Activity, Role, Skill
        target_id TEXT NOT NULL,
        target_type TEXT NOT NULL,
        relationship TEXT NOT NULL -- HAS_ACTIVITY, PERFORMED_BY, REQUIRES_SKILL, IMPACTS
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_interventions (
        id TEXT PRIMARY KEY,
        activity_id TEXT,
        capability_name TEXT NOT NULL,
        impact_description TEXT,
        evidence TEXT,
        FOREIGN KEY(activity_id) REFERENCES activities(id)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", DB_PATH)
