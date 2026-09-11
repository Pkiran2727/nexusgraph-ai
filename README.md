---
title: NexusGraph AI
emoji: 🌐
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
app_port: 7860
short_description: Enterprise Process x Role x Skill Intelligence Engine
---

# NexusGraph AI — Enterprise Process × Role × Skill Intelligence Engine

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/AI-Gemini_3.1_Flash--Lite-orange.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**NexusGraph AI** is a full-stack Enterprise AI application built for the **Modus Enterprise AI Build Challenge (Assignment 11: Process × Role × Skill Intelligence Graph & Assignment 4: Role Intelligence)**.

It creates a multi-dimensional digital twin of an enterprise—linking Processes, Activities, Job Roles, and Skills into an interactive, visual graph. The platform allows enterprise leaders to simulate the **cascading ripple effects** of AI automation on job roles and workforce skill requirements in real time.

---

## 🌟 Key Features

* **Interactive Network Graph (Cytoscape.js):** Visual canvas rendering directional relationships across Value Chains, Processes, Activities, Roles, and Skills.
* **Cascading Impact Simulator:** Select any business activity to simulate AI automation and instantly trace downstream impacts on employee roles and skill obsolescence.
* **Assignment 4 Role Intelligence:** AI exposure scoring, role vulnerability analysis, and automated reskilling recommendations.
* **Surprise Record Live Ingestion:** Ingest unstructured business scenarios live using **Google Gemini 3.1 Flash-Lite** with Pydantic JSON schema validation and automatic SQLite persistence.
* **Deterministic Math + AI Split:** Graph traversals and impact calculations are 100% deterministic (NetworkX), while AI is reserved for qualitative reasoning and text parsing.
* **Pastel UI Design System:** Premium, modern single-page dashboard interface with interactive side drawers.

---

## 🏗️ 5-Layer Architecture

1. **Layer 1 (UI Visual Canvas):** SPA with Cytoscape.js visual graph renderer and soft pastel design system.
2. **Layer 2 (API Gateway):** FastAPI asynchronous REST server (`backend/main.py`).
3. **Layer 3 (AI Intelligence Engine):** Gemini 3.1 Flash-Lite integration (`backend/ai_agent.py`) with Pydantic validation.
4. **Layer 4 (Graph Analytics Engine):** NetworkX Python engine (`backend/graph_engine.py`) for deterministic impact calculations.
5. **Layer 5 (Persistence Layer):** SQLite relational database (`data/nexus_intelligence.db`).

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
* Python 3.10+
* Google Gemini API Key

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Pkiran2727/nexusgraph-ai.git
cd nexusgraph-ai

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `backend/.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8095
HOST=0.0.0.0
```

### 4. Run Application Server
```bash
python backend/main.py
```
Open your browser and navigate to: `http://localhost:8095`

---

## 🧪 Testing & Quality Assurance

Run the automated test suites:

```bash
# Run backend unit tests (Pytest)
pytest tests/test_backend.py

# Run E2E browser automation tests (Selenium)
pytest tests/test_selenium_e2e.py
```

---

## 📄 Documentation

* [ASSIGNMENT_11_SUBMISSION_REPORT.md](ASSIGNMENT_11_SUBMISSION_REPORT.md) — Comprehensive technical submission report and Q&A defense.
* [TEST_CASES_AND_BUG_REPORT.md](TEST_CASES_AND_BUG_REPORT.md) — QA execution matrix, test cases, and bug report.
