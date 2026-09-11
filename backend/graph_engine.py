import sqlite3
import networkx as nx
from database import DB_PATH

class NexusGraphEngine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.graph = nx.DiGraph()
        self.reload_graph()

    def reload_graph(self):
        self.graph.clear()
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Add Nodes with Pastel Colors
        cursor.execute("SELECT id, name, business_purpose, automation_potential FROM processes")
        for row in cursor.fetchall():
            self.graph.add_node(row["id"], label=row["name"], type="Process", color="#7dd3fc", size=36, details=dict(row)) # Pastel sky blue

        cursor.execute("SELECT id, name, execution_mode, ai_exposure FROM activities")
        for row in cursor.fetchall():
            self.graph.add_node(row["id"], label=row["name"], type="Activity", color="#fcd34d", size=26, details=dict(row)) # Pastel amber

        cursor.execute("SELECT id, name, department, seniority, future_risk_score, summary FROM roles")
        for row in cursor.fetchall():
            self.graph.add_node(row["id"], label=row["name"], type="Role", color="#c084fc", size=32, details=dict(row)) # Pastel lavender/purple

        cursor.execute("SELECT id, name, category, trend FROM skills")
        for row in cursor.fetchall():
            self.graph.add_node(row["id"], label=row["name"], type="Skill", color="#6ee7b7", size=24, details=dict(row)) # Pastel mint emerald

        # Add Edges
        cursor.execute("SELECT source_id, target_id, relationship FROM graph_edges")
        for row in cursor.fetchall():
            if self.graph.has_node(row["source_id"]) and self.graph.has_node(row["target_id"]):
                self.graph.add_edge(row["source_id"], row["target_id"], relationship=row["relationship"])

        conn.close()

    def get_cytoscape_elements(self):
        elements = {"nodes": [], "edges": []}

        for node_id, data in self.graph.nodes(data=True):
            elements["nodes"].append({
                "data": {
                    "id": node_id,
                    "label": data.get("label", node_id),
                    "type": data.get("type", "Unknown"),
                    "color": data.get("color", "#94a3b8"),
                    "size": data.get("size", 25),
                    "details": data.get("details", {})
                }
            })

        for source, target, data in self.graph.edges(data=True):
            elements["edges"].append({
                "data": {
                    "id": f"{source}_{target}",
                    "source": source,
                    "target": target,
                    "relationship": data.get("relationship", "CONNECTED")
                }
            })

        return elements

    def get_role_intelligence(self, role_id):
        """Assignment 4: Deep process-to-role intelligence calculation"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM roles WHERE id = ?", (role_id,))
        role = cursor.fetchone()
        if not role:
            # Fallback search by name
            cursor.execute("SELECT * FROM roles WHERE lower(name) LIKE lower(?)", (f"%{role_id}%",))
            role = cursor.fetchone()

        if not role:
            conn.close()
            return None

        role_dict = dict(role)
        role_actual_id = role_dict["id"]

        # Get activities performed by this role
        cursor.execute("""
        SELECT a.*, p.name as process_name, p.id as process_id
        FROM activities a
        JOIN graph_edges e ON e.source_id = a.id
        JOIN processes p ON a.process_id = p.id
        WHERE e.target_id = ? AND e.relationship = 'PERFORMED_BY'
        """, (role_actual_id,))
        activities = [dict(r) for r in cursor.fetchall()]

        # Get processes involving this role directly
        processes = list({a["process_name"]: a["process_id"] for a in activities}.items())

        # Get skills required by this role
        cursor.execute("""
        SELECT s.*
        FROM skills s
        JOIN graph_edges e ON e.target_id = s.id
        WHERE e.source_id = ? AND e.relationship = 'REQUIRES_SKILL'
        """, (role_actual_id,))
        skills = [dict(r) for r in cursor.fetchall()]

        # AI impact breakdown
        automated_acts = [a for a in activities if a["execution_mode"] == "Automated" or a["ai_exposure"] == "High"]
        augmented_acts = [a for a in activities if a["execution_mode"] == "Hybrid" or a["ai_exposure"] == "Medium"]

        declining_skills = [s for s in skills if s["trend"] == "Declining"]
        emerging_skills = [s for s in skills if s["trend"] in ["Emerging", "AI-Augmented"]]

        conn.close()

        exposure_score = round((len(automated_acts) + len(augmented_acts)*0.5) / max(1, len(activities)) * 100, 1)

        # Assignment 4 Reasoning Chain:
        # Processes -> Activities -> AI Impact -> Future Responsibilities -> Resulting Role Change
        reasoning_chain = {
            "involved_processes": [p[0] for p in processes],
            "activities_performed": [a["name"] for a in activities],
            "ai_impact_summary": f"High exposure to automated workflow tools across {len(automated_acts)} activities and AI augmentation in {len(augmented_acts)} activities.",
            "future_responsibilities": [
                f"Shift from manual execution of {a['name']} to AI model supervision and anomaly verification" for a in automated_acts
            ] + ["Strategic decision making and stakeholder negotiation"],
            "resulting_role_change": f"Role transitions to an AI-Augmented Specialist profile with {exposure_score}% workflow automation."
        }

        return {
            "role": role_dict,
            "activities_count": len(activities),
            "processes": processes,
            "activities": activities,
            "skills": skills,
            "automated_activities": automated_acts,
            "augmented_activities": augmented_acts,
            "declining_skills": declining_skills,
            "emerging_skills": emerging_skills,
            "ai_exposure_percentage": exposure_score,
            "reasoning_chain": reasoning_chain
        }

    def get_roles_by_skill(self, skill_id):
        """Assignment 11 Navigation: Select a skill -> see every role requiring that skill"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT r.*
        FROM roles r
        JOIN graph_edges e ON e.source_id = r.id
        WHERE e.target_id = ? AND e.relationship = 'REQUIRES_SKILL'
        """, (skill_id,))

        roles = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return roles

    def get_roles_by_process(self, process_id):
        """Assignment 11 Navigation: Select a process -> see affected roles"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT DISTINCT r.*
        FROM roles r
        JOIN graph_edges e1 ON e1.target_id = r.id AND e1.relationship = 'PERFORMED_BY'
        JOIN activities a ON a.id = e1.source_id
        WHERE a.process_id = ?
        """, (process_id,))

        roles = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return roles

    def simulate_cascading_impact(self, activity_id):
        """Assignment 11: Cascading visual impact simulation across nodes"""
        if not self.graph.has_node(activity_id):
            return {"error": "Activity not found"}

        processes_affected = []
        roles_affected = []
        skills_affected = []

        for predecessor in self.graph.predecessors(activity_id):
            if self.graph.nodes[predecessor].get("type") == "Process":
                processes_affected.append(predecessor)

        for successor in self.graph.successors(activity_id):
            node_type = self.graph.nodes[successor].get("type")
            if node_type == "Role":
                roles_affected.append(successor)
                for role_successor in self.graph.successors(successor):
                    if self.graph.nodes[role_successor].get("type") == "Skill":
                        skills_affected.append(role_successor)

        highlight_ids = list(set([activity_id] + processes_affected + roles_affected + skills_affected))

        return {
            "trigger_activity": activity_id,
            "processes_impacted": processes_affected,
            "roles_impacted": roles_affected,
            "skills_impacted": list(set(skills_affected)),
            "highlight_node_ids": highlight_ids
        }
