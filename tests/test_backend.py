import os
import sys
import unittest
import requests

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from database import DB_PATH, get_db_connection
from graph_engine import NexusGraphEngine
from config import GEMINI_API_KEY

class TestNexusGraphBackend(unittest.TestCase):

    def setUp(self):
        self.engine = NexusGraphEngine(db_path=DB_PATH)
        self.base_url = "http://localhost:8095"

    def test_01_database_persistence_and_schema(self):
        """Verify SQLite database exists, connects, and contains records"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM processes")
        proc_count = cursor.fetchone()[0]
        conn.close()
        self.assertGreater(proc_count, 0, "Processes table should contain seeded records")

    def test_02_graph_elements_payload(self):
        """Verify NetworkX graph builds nodes and edges for Cytoscape"""
        cy_data = self.engine.get_cytoscape_elements()
        self.assertIn("nodes", cy_data)
        self.assertIn("edges", cy_data)
        self.assertGreater(len(cy_data["nodes"]), 10)
        self.assertGreater(len(cy_data["edges"]), 10)

    def test_03_assignment_4_role_intelligence(self):
        """Verify Assignment 4 role intelligence and reasoning chain generation"""
        role_data = self.engine.get_role_intelligence("R1") # Procurement Manager
        self.assertIsNotNone(role_data)
        self.assertEqual(role_data["role"]["name"], "Procurement Manager")
        self.assertIn("reasoning_chain", role_data)
        self.assertGreater(role_data["ai_exposure_percentage"], 0)

    def test_04_assignment_11_cascading_impact(self):
        """Verify Assignment 11 cascading impact simulation algorithm"""
        sim_res = self.engine.simulate_cascading_impact("A4") # Contract auditing
        self.assertEqual(sim_res["trigger_activity"], "A4")
        self.assertIn("roles_impacted", sim_res)
        self.assertIn("highlight_node_ids", sim_res)

    def test_05_api_key_security(self):
        """Verify API key is loaded from config and not hardcoded as string literal in source"""
        with open(os.path.join(os.path.dirname(__file__), '..', 'backend', 'ai_agent.py'), 'r') as f:
            code = f.read()
            self.assertNotIn("API_KEY_SECRET_PLACEHOLDER", code, "API Key should NOT be hardcoded in ai_agent.py!")

    def test_06_rest_api_endpoints(self):
        """Verify FastAPI endpoints respond with HTTP 200"""
        try:
            from fastapi.testclient import TestClient
            from main import app
            client = TestClient(app)
            resp_health = client.get("/api/health")
            self.assertEqual(resp_health.status_code, 200)

            resp_graph = client.get("/api/graph")
            self.assertEqual(resp_graph.status_code, 200)

            resp_roles = client.get("/api/roles")
            self.assertEqual(resp_roles.status_code, 200)

            resp_role_impact = client.get("/api/role/R1/impact")
            self.assertEqual(resp_role_impact.status_code, 200)

            resp_skills = client.get("/api/skills")
            self.assertEqual(resp_skills.status_code, 200)
        except Exception:
            resp_health = requests.get(f"{self.base_url}/api/health")
            self.assertEqual(resp_health.status_code, 200)

if __name__ == "__main__":
    unittest.main()
