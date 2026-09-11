async function loadRoleOptions() {
    try {
        const res = await fetch('/api/roles');
        const roles = await res.json();
        const selector = document.getElementById('role-selector');
        if (!selector) return;

        selector.innerHTML = '';
        roles.forEach(r => {
            const opt = document.createElement('option');
            opt.value = r.id;
            opt.textContent = `${r.name} (${r.department})`;
            selector.appendChild(opt);
        });
    } catch (e) {
        console.error("Failed to load role options:", e);
    }
}

async function loadSkillOptions() {
    try {
        const res = await fetch('/api/skills');
        const skills = await res.json();
        const selector = document.getElementById('skill-selector');
        if (!selector) return;

        selector.innerHTML = '';
        skills.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s.id;
            opt.textContent = `${s.name} [${s.category}]`;
            selector.appendChild(opt);
        });
    } catch (e) {
        console.error("Failed to load skill options:", e);
    }
}

async function analyzeSelectedRole(roleId) {
    const resultsContainer = document.getElementById('role-analysis-results');
    if (!resultsContainer) return;

    resultsContainer.innerHTML = '<p style="color:var(--text-muted);">Analyzing process-to-role connections...</p>';

    try {
        const res = await fetch(`/api/role/${roleId}/impact`);
        if (!res.ok) throw new Error("Role impact API failed");
        const data = await res.json();

        const role = data.role;
        const exposure = data.ai_exposure_percentage;
        const chain = data.reasoning_chain || {};

        let actsHtml = data.activities.map(a => `
            <div style="padding:0.65rem 0.85rem; background:rgba(255,255,255,0.03); border:1px solid var(--border-color); border-radius:8px; margin-bottom:0.5rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:var(--pastel-amber); font-size:0.9rem;">${a.name}</strong>
                    <span class="badge badge-amber">${a.execution_mode}</span>
                </div>
                <div style="font-size:0.775rem; color:var(--text-muted); margin-top:0.25rem;">Process: ${a.process_name}</div>
            </div>
        `).join('');

        let skillsHtml = data.skills.map(s => `
            <span class="pill" style="border-color:${s.trend === 'Declining' ? 'rgba(254, 205, 211, 0.4)' : 'rgba(167, 243, 208, 0.4)'};">
                ${s.name} (${s.trend})
            </span>
        `).join('');

        let reasoningHtml = `
            <div style="background:rgba(233, 213, 255, 0.08); border:1px solid rgba(233, 213, 255, 0.25); border-radius:10px; padding:1rem; margin-top:1.25rem;">
                <h4 style="color:var(--pastel-lavender); font-size:0.9rem; margin-bottom:0.5rem;">Assignment 4 Reasoning Chain:</h4>
                <div style="font-size:0.825rem; color:var(--text-subtle); line-height:1.5;">
                    • <strong>Involved Processes:</strong> ${(chain.involved_processes || []).join(', ')}<br>
                    • <strong>Activities Performed:</strong> ${(chain.activities_performed || []).join(', ')}<br>
                    • <strong>AI Exposure Summary:</strong> ${chain.ai_impact_summary || ''}<br>
                    • <strong>Resulting Role Change:</strong> ${chain.resulting_role_change || ''}
                </div>
            </div>
        `;

        resultsContainer.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:1px solid var(--border-color); padding-bottom:1rem; margin-bottom:1.25rem;">
                <div>
                    <h2 style="font-size:1.4rem; font-family:'Outfit', sans-serif; color:var(--pastel-lavender);">${role.name}</h2>
                    <span style="font-size:0.825rem; color:var(--text-muted);">${role.department} Department • ${role.seniority} Level</span>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">AI Exposure Index</div>
                    <div style="font-size:1.6rem; font-weight:700; color:var(--pastel-rose);">${exposure}%</div>
                </div>
            </div>

            <p style="font-size:0.875rem; line-height:1.5; color:var(--text-subtle); margin-bottom:1.25rem;">${role.summary}</p>

            <div class="progress-container">
                <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:500;">
                    <span style="color:var(--text-muted);">Workflow Automation Exposure</span>
                    <span style="color:var(--pastel-rose);">${exposure}% Exposure</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: ${exposure}%;"></div>
                </div>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin-top:1.5rem;">
                <div>
                    <h4 style="font-size:0.9rem; margin-bottom:0.65rem; color:var(--pastel-amber);">Performed Activities (${data.activities_count})</h4>
                    ${actsHtml || '<p style="font-size:0.8rem; color:var(--text-muted);">No direct activities linked.</p>'}
                </div>
                <div>
                    <h4 style="font-size:0.9rem; margin-bottom:0.65rem; color:var(--pastel-mint);">Skill Capability Requirements</h4>
                    <div class="pill-group">${skillsHtml || '<p style="font-size:0.8rem; color:var(--text-muted);">No skills linked.</p>'}</div>
                </div>
            </div>

            ${reasoningHtml}
        `;

    } catch (e) {
        resultsContainer.innerHTML = `<p style="color:var(--pastel-rose);">Error analyzing role: ${e.message}</p>`;
    }
}

async function analyzeSelectedSkill(skillId) {
    const resultsContainer = document.getElementById('role-analysis-results');
    if (!resultsContainer) return;

    resultsContainer.innerHTML = '<p style="color:var(--text-muted);">Looking up roles requiring skill...</p>';

    try {
        const res = await fetch(`/api/skill/${skillId}/roles`);
        const data = await res.json();

        let rolesHtml = data.roles.map(r => `
            <div style="padding:0.75rem 1rem; background:rgba(255,255,255,0.03); border:1px solid var(--border-color); border-radius:10px; margin-bottom:0.65rem;">
                <div style="font-weight:600; color:var(--pastel-lavender); font-size:0.95rem;">${r.name}</div>
                <div style="font-size:0.8rem; color:var(--text-muted);">${r.department} • ${r.seniority}</div>
            </div>
        `).join('');

        resultsContainer.innerHTML = `
            <h3 class="panel-title" style="color:var(--pastel-sky);">Assignment 11 Skill Navigation</h3>
            <p style="color:var(--text-muted); font-size:0.875rem; margin-bottom:1.25rem;">Found <strong>${data.count}</strong> organizational roles requiring skill ID <code>${skillId}</code>:</p>
            ${rolesHtml || '<p style="color:var(--text-muted);">No roles require this specific skill.</p>'}
        `;

    } catch (e) {
        resultsContainer.innerHTML = `<p style="color:var(--pastel-rose);">Skill lookup failed: ${e.message}</p>`;
    }
}
