import sqlite3
from database import DB_PATH, init_db

def seed_database():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear existing records
    tables = ["ai_interventions", "graph_edges", "skills", "roles", "activities", "processes", "value_chains"]
    for t in tables:
        cursor.execute(f"DELETE FROM {t};")

    # 1. Value Chain
    cursor.execute("""
    INSERT INTO value_chains (id, name, industry, description) VALUES
    ('VC1', 'Global Enterprise Supply Chain & Operations', 'Logistics & Manufacturing', 'End-to-end procurement, manufacturing, warehousing, and distribution value chain');
    """)

    # 2. Processes (Assignment 11 & 4 Process Library)
    processes = [
        ('P1', 'VC1', 'Demand Forecasting & Replenishment', 'Predicting customer demand and optimizing stock reorder points', 'High', 'AI-Driven with Human Oversight'),
        ('P2', 'VC1', 'Supplier Evaluation & Procurement', 'Evaluating vendor proposals, negotiating SLAs, and executing contracts', 'Medium', 'Hybrid AI-Augmented Negotiations'),
        ('P3', 'VC1', 'Warehouse Inventory Optimization', 'Real-time stock tracking, slotting, and automated replenishment', 'High', 'Autonomous Warehouse Robotics & AI'),
        ('P4', 'VC1', 'Quality Control & Defect Detection', 'Inspecting incoming components and finished goods for flaws', 'High', 'Computer Vision Automated Inspection'),
        ('P5', 'VC1', 'Dynamic Fleet & Route Optimization', 'Optimizing delivery routes considering traffic, fuel, and ETA', 'High', 'Real-time Algorithmic Dispatch'),
        ('P6', 'VC1', 'Customer Order Fulfillment & Returns', 'Managing order processing, reverse logistics, and customer claims', 'Medium', 'Agentic Resolution & Human Exception Handling'),
        ('P7', 'VC1', 'ESG & Sustainable Sourcing Governance', 'Monitoring carbon footprints, ethical sourcing, and supplier compliance', 'Medium', 'AI Compliance Analytics & Human Strategy')
    ]
    cursor.executemany("INSERT INTO processes VALUES (?,?,?,?,?,?);", processes)

    # 3. Activities
    activities = [
        ('A1', 'P1', 'Historical Sales Trend Analysis', 'Automated', 'High'),
        ('A2', 'P1', 'Seasonal & Macro Anomaly Modeling', 'Automated', 'High'),
        ('A3', 'P2', 'Vendor RFQ Generation & Evaluation', 'Hybrid', 'Medium'),
        ('A4', 'P2', 'Contract Clause Risk Auditing', 'Hybrid', 'High'),
        ('A5', 'P3', 'Safety Stock & Buffer Calculation', 'Automated', 'High'),
        ('A6', 'P4', 'Automated Visual Defect Inspection', 'Automated', 'High'),
        ('A7', 'P5', 'Dynamic Route Re-calculation', 'Automated', 'High'),
        ('A8', 'P6', 'Claims Fraud Detection & Processing', 'Hybrid', 'Medium'),
        ('A9', 'P7', 'Supplier Carbon Footprint Audit', 'Hybrid', 'Medium')
    ]
    cursor.executemany("INSERT INTO activities VALUES (?,?,?,?,?);", activities)

    # 4. Roles (Assignment 4 Role Catalog)
    roles = [
        ('R1', 'Procurement Manager', 'Supply Chain', 'Manager', 0.65, 'Responsible for vendor relationships, contract negotiation, and material sourcing strategy. High shift toward AI-augmented vendor intelligence.'),
        ('R2', 'Demand Analyst', 'Operations', 'Senior Specialist', 0.75, 'Analyzes sales signals and generates reorder forecasts. Shifting from manual spreadsheets to supervising predictive ML engines.'),
        ('R3', 'Logistics & Fleet Coordinator', 'Logistics', 'Specialist', 0.60, 'Coordinates dispatch and shipment schedules. Transitioning to exception handling as dynamic routing automates dispatch.'),
        ('R4', 'Quality Assurance Inspector', 'Manufacturing', 'Specialist', 0.80, 'Inspects physical goods. Transitioning to supervising Computer Vision AI defect detection hardware.'),
        ('R5', 'Sustainability & Governance Officer', 'ESG', 'Director', 0.35, 'Ensures ethical sourcing and environmental compliance. High strategic human capability with AI reporting tools.')
    ]
    cursor.executemany("INSERT INTO roles VALUES (?,?,?,?,?,?);", roles)

    # 5. Skills (Assignment 11 Skill Catalog)
    skills = [
        ('S1', 'Manual Spreadsheet Modeling', 'Operational', 'Declining'),
        ('S2', 'Predictive Machine Learning Supervision', 'Technical', 'Emerging'),
        ('S3', 'Strategic Supplier Negotiation', 'Strategic', 'Enduring'),
        ('S4', 'Automated Contract Risk Auditing', 'Technical', 'AI-Augmented'),
        ('S5', 'Computer Vision Defect Analysis', 'Technical', 'Emerging'),
        ('S6', 'Algorithmic Route & Fleet Planning', 'Technical', 'Increasing'),
        ('S7', 'ESG Regulatory Compliance Strategy', 'Strategic', 'Increasing'),
        ('S8', 'AI Prompt & Agent Engineering', 'Technical', 'Emerging'),
        ('S9', 'Cross-Functional Stakeholder Communication', 'Soft', 'Enduring')
    ]
    cursor.executemany("INSERT INTO skills VALUES (?,?,?,?);", skills)

    # 6. Graph Edges (Connecting Process -> Activity -> Role -> Skill)
    edges = [
        # Process -> Activity
        ('P1', 'Process', 'A1', 'Activity', 'HAS_ACTIVITY'),
        ('P1', 'Process', 'A2', 'Activity', 'HAS_ACTIVITY'),
        ('P2', 'Process', 'A3', 'Activity', 'HAS_ACTIVITY'),
        ('P2', 'Process', 'A4', 'Activity', 'HAS_ACTIVITY'),
        ('P3', 'Process', 'A5', 'Activity', 'HAS_ACTIVITY'),
        ('P4', 'Process', 'A6', 'Activity', 'HAS_ACTIVITY'),
        ('P5', 'Process', 'A7', 'Activity', 'HAS_ACTIVITY'),
        ('P6', 'Process', 'A8', 'Activity', 'HAS_ACTIVITY'),
        ('P7', 'Process', 'A9', 'Activity', 'HAS_ACTIVITY'),

        # Activity -> Role
        ('A1', 'Activity', 'R2', 'Role', 'PERFORMED_BY'),
        ('A2', 'Activity', 'R2', 'Role', 'PERFORMED_BY'),
        ('A3', 'Activity', 'R1', 'Role', 'PERFORMED_BY'),
        ('A4', 'Activity', 'R1', 'Role', 'PERFORMED_BY'),
        ('A5', 'Activity', 'R2', 'Role', 'PERFORMED_BY'),
        ('A6', 'Activity', 'R4', 'Role', 'PERFORMED_BY'),
        ('A7', 'Activity', 'R3', 'Role', 'PERFORMED_BY'),
        ('A8', 'Activity', 'R3', 'Role', 'PERFORMED_BY'),
        ('A9', 'Activity', 'R5', 'Role', 'PERFORMED_BY'),

        # Role -> Skill
        ('R1', 'Role', 'S3', 'Skill', 'REQUIRES_SKILL'),
        ('R1', 'Role', 'S4', 'Skill', 'REQUIRES_SKILL'),
        ('R1', 'Role', 'S8', 'Skill', 'REQUIRES_SKILL'),
        ('R1', 'Role', 'S9', 'Skill', 'REQUIRES_SKILL'),

        ('R2', 'Role', 'S1', 'Skill', 'REQUIRES_SKILL'),
        ('R2', 'Role', 'S2', 'Skill', 'REQUIRES_SKILL'),
        ('R2', 'Role', 'S8', 'Skill', 'REQUIRES_SKILL'),

        ('R3', 'Role', 'S6', 'Skill', 'REQUIRES_SKILL'),
        ('R3', 'Role', 'S9', 'Skill', 'REQUIRES_SKILL'),

        ('R4', 'Role', 'S5', 'Skill', 'REQUIRES_SKILL'),
        ('R4', 'Role', 'S8', 'Skill', 'REQUIRES_SKILL'),

        ('R5', 'Role', 'S7', 'Skill', 'REQUIRES_SKILL'),
        ('R5', 'Role', 'S9', 'Skill', 'REQUIRES_SKILL')
    ]
    cursor.executemany("INSERT INTO graph_edges (source_id, source_type, target_id, target_type, relationship) VALUES (?,?,?,?,?);", edges)

    # 7. AI Interventions
    interventions = [
        ('AI1', 'A1', 'LLM Time-Series Forecasting Agent', 'Automatically parses past demand logs and macro-economic signals to generate 95% accurate stock reorder points.', 'Reduces stockouts by 42% in pilot implementations.'),
        ('AI2', 'A4', 'Legal Contract LLM Parser', 'Scans incoming 50-page vendor contracts in seconds to flag non-standard liability clauses.', 'Cuts contract audit time from 4 hours to 3 minutes.'),
        ('AI3', 'A6', 'Edge Vision Defect Detection Model', 'Captures 60 frames per second on conveyor belts to detect sub-millimeter component defects.', 'Achieves 99.4% defect detection rate compared to 88% human manual check.'),
        ('AI4', 'A7', 'Real-Time Genetic Route Optimizer', 'Re-routes drivers dynamically using live traffic, weather, and battery degradation APIs.', 'Decreases transit fuel cost by 18%.')
    ]
    cursor.executemany("INSERT INTO ai_interventions VALUES (?,?,?,?,?);", interventions)

    conn.commit()
    conn.close()
    print("Database successfully seeded with enterprise supply chain graph!")

if __name__ == "__main__":
    seed_database()
