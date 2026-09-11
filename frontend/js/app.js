document.addEventListener('DOMContentLoaded', async () => {
    await loadInitialGraph();
    await loadRoleOptions();
    await loadSkillOptions();

    setupTabs();
    setupGraphControls();
    setupSimulator();
    setupSurpriseIngestion();
});

async function loadInitialGraph() {
    try {
        const res = await fetch('/api/graph');
        const elementsData = await res.json();

        const nodes = elementsData.nodes || [];
        let pCount = 0, aCount = 0, rCount = 0, sCount = 0;

        nodes.forEach(n => {
            const t = n.data.type;
            if (t === 'Process') pCount++;
            if (t === 'Activity') aCount++;
            if (t === 'Role') rCount++;
            if (t === 'Skill') sCount++;
        });

        document.getElementById('stat-processes').textContent = pCount;
        document.getElementById('stat-activities').textContent = aCount;
        document.getElementById('stat-roles').textContent = rCount;
        document.getElementById('stat-skills').textContent = sCount;

        initGraph(elementsData);

    } catch (e) {
        console.error("Failed to load initial graph:", e);
    }
}

function setupTabs() {
    const btns = document.querySelectorAll('.tab-btn');
    btns.forEach(btn => {
        btn.addEventListener('click', () => {
            btns.forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));

            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            document.getElementById(targetId).classList.add('active');

            if (targetId === 'tab-graph' && cy) {
                setTimeout(() => cy.resize(), 100);
            }
        });
    });
}

function setupGraphControls() {
    document.getElementById('btn-reset-layout')?.addEventListener('click', () => runLayout('cose'));
    document.getElementById('btn-layout-circle')?.addEventListener('click', () => runLayout('circle'));
    document.getElementById('btn-layout-concentric')?.addEventListener('click', () => runLayout('concentric'));

    document.getElementById('btn-analyze-role')?.addEventListener('click', () => {
        const selector = document.getElementById('role-selector');
        if (selector && selector.value) {
            analyzeSelectedRole(selector.value);
        }
    });

    document.getElementById('btn-analyze-skill')?.addEventListener('click', () => {
        const selector = document.getElementById('skill-selector');
        if (selector && selector.value) {
            analyzeSelectedSkill(selector.value);
        }
    });
}

function setupSimulator() {
    document.getElementById('btn-run-simulation')?.addEventListener('click', async () => {
        const actId = document.getElementById('activity-simulator-selector').value;
        const container = document.getElementById('simulation-results');

        container.innerHTML = '<p style="color:var(--text-muted);">Calculating cascading network ripple effect...</p>';

        try {
            const res = await fetch('/api/simulate-impact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ activity_id: actId })
            });

            const data = await res.json();

            if (cy && data.highlight_node_ids) {
                cy.nodes().removeClass('highlighted');
                data.highlight_node_ids.forEach(id => {
                    cy.getElementById(id).addClass('highlighted');
                });
            }

            container.innerHTML = `
                <div style="margin-bottom:1.25rem;">
                    <h4 style="color:var(--pastel-amber); font-size:1.15rem; margin-bottom:0.35rem;">Trigger Activity: ${data.trigger_activity}</h4>
                    <p style="font-size:0.85rem; color:var(--text-muted);">AI Automation applied to activity. Cascading network nodes highlighted in pastel rose on canvas.</p>
                </div>

                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1.25rem;">
                    <div style="background:rgba(255,255,255,0.03); padding:1rem; border-radius:10px; border:1px solid var(--border-color);">
                        <div style="font-size:0.75rem; color:var(--pastel-sky); text-transform:uppercase; font-weight:600;">Impacted Processes</div>
                        <div style="font-size:1.5rem; font-weight:700; margin-top:0.35rem; color:var(--pastel-sky);">${data.processes_impacted.length}</div>
                        <div style="font-size:0.775rem; color:var(--text-muted); margin-top:0.25rem;">${data.processes_impacted.join(', ')}</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.03); padding:1rem; border-radius:10px; border:1px solid var(--border-color);">
                        <div style="font-size:0.75rem; color:var(--pastel-lavender); text-transform:uppercase; font-weight:600;">Impacted Roles</div>
                        <div style="font-size:1.5rem; font-weight:700; margin-top:0.35rem; color:var(--pastel-lavender);">${data.roles_impacted.length}</div>
                        <div style="font-size:0.775rem; color:var(--text-muted); margin-top:0.25rem;">${data.roles_impacted.join(', ')}</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.03); padding:1rem; border-radius:10px; border:1px solid var(--border-color);">
                        <div style="font-size:0.75rem; color:var(--pastel-mint); text-transform:uppercase; font-weight:600;">Impacted Skills</div>
                        <div style="font-size:1.5rem; font-weight:700; margin-top:0.35rem; color:var(--pastel-mint);">${data.skills_impacted.length}</div>
                        <div style="font-size:0.775rem; color:var(--text-muted); margin-top:0.25rem;">${data.skills_impacted.join(', ')}</div>
                    </div>
                </div>
            `;

        } catch (e) {
            container.innerHTML = `<p style="color:var(--pastel-rose);">Simulation failed: ${e.message}</p>`;
        }
    });
}

function setupSurpriseIngestion() {
    document.getElementById('btn-ingest-surprise')?.addEventListener('click', async () => {
        const type = document.getElementById('surprise-type').value;
        const name = document.getElementById('surprise-name').value;
        const context = document.getElementById('surprise-context').value;
        const container = document.getElementById('surprise-results');

        if (!name) {
            alert("Please enter a name for the surprise record.");
            return;
        }

        container.innerHTML = '<p style="color:var(--pastel-sky);">Gemini AI Agent decomposing and persisting record...</p>';

        try {
            const res = await fetch('/api/ingest-surprise-record', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ record_type: type, name: name, context: context })
            });

            const data = await res.json();

            if (data.updated_graph) {
                initGraph(data.updated_graph);
                await loadInitialGraph();
                await loadRoleOptions();
                await loadSkillOptions();
            }

            const item = data.data;
            container.innerHTML = `
                <div style="background:rgba(167, 243, 208, 0.1); border:1px solid rgba(167, 243, 208, 0.35); padding:1.15rem; border-radius:10px; margin-bottom:1.25rem;">
                    <h4 style="color:var(--pastel-mint); margin-bottom:0.35rem; font-size:1rem;">✓ Ingestion Successful & Persisted to SQLite</h4>
                    <p style="font-size:0.875rem; color:var(--text-subtle);">${data.message}</p>
                </div>
                <div style="font-size:0.875rem; color:var(--text-main); line-height:1.6;">
                    <strong>Generated Record ID:</strong> <code>${item.id_prefix}</code><br>
                    <strong>Purpose/Description:</strong> ${item.description_or_purpose}<br>
                    <strong>AI Exposure Level:</strong> <span class="badge badge-rose">${item.automation_or_exposure}</span>
                </div>
                <div style="margin-top:1rem; font-size:0.825rem; color:var(--text-subtle); background:rgba(255,255,255,0.03); padding:1rem; border-radius:8px; border:1px solid var(--border-color); line-height:1.5;">
                    <strong style="color:var(--pastel-sky);">AI Agent Reasoning:</strong> ${item.reasoning}
                </div>
            `;

        } catch (e) {
            container.innerHTML = `<p style="color:var(--pastel-rose);">Ingestion error: ${e.message}</p>`;
        }
    });
}
