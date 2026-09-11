let cy = null;

function initGraph(elementsData) {
    if (cy) {
        cy.destroy();
    }

    cy = cytoscape({
        container: document.getElementById('cy'),
        elements: elementsData,
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': 'data(color)',
                    'label': 'data(label)',
                    'color': '#f8fafc',
                    'font-size': '11px',
                    'font-weight': '600',
                    'text-valign': 'bottom',
                    'text-margin-y': '6px',
                    'width': 'data(size)',
                    'height': 'data(size)',
                    'border-width': '2px',
                    'border-color': 'rgba(255, 255, 255, 0.5)',
                    'transition-property': 'background-color, border-color, width, height',
                    'transition-duration': '0.3s'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'line-color': 'rgba(255, 255, 255, 0.18)',
                    'target-arrow-color': 'rgba(255, 255, 255, 0.35)',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'opacity': 0.75
                }
            },
            {
                selector: '.highlighted',
                style: {
                    'border-color': '#fecdd3',
                    'border-width': '4px',
                    'shadow-blur': 15,
                    'shadow-color': '#fecdd3'
                }
            }
        ],
        layout: {
            name: 'cose',
            animate: true,
            padding: 30,
            componentSpacing: 45
        }
    });

    cy.on('tap', 'node', function(evt){
        const node = evt.target;
        const data = node.data();
        renderNodeInspector(data);
    });

    return cy;
}

function renderNodeInspector(data) {
    const inspector = document.getElementById('inspector-content');
    if (!inspector) return;

    let badgeClass = 'badge-sky';
    if (data.type === 'Activity') badgeClass = 'badge-amber';
    if (data.type === 'Role') badgeClass = 'badge-lavender';
    if (data.type === 'Skill') badgeClass = 'badge-mint';

    let detailsHtml = '';
    if (data.details) {
        for (const [key, val] of Object.entries(data.details)) {
            if (key !== 'id' && key !== 'name') {
                detailsHtml += `<div style="margin-top:0.5rem; word-break:break-word;"><strong style="color:var(--text-muted); font-size:0.75rem; text-transform:uppercase;">${key.replace('_', ' ')}:</strong> <span style="font-size:0.875rem; color:var(--text-subtle);">${val}</span></div>`;
            }
        }
    }

    inspector.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.85rem;">
            <h4 style="font-size:1.15rem; color:var(--text-main); font-weight:600;">${data.label}</h4>
            <span class="badge ${badgeClass}">${data.type}</span>
        </div>
        <div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:1rem;">ID: <code>${data.id}</code></div>
        <div style="border-top:1px solid var(--border-color); padding-top:0.85rem;">
            ${detailsHtml}
        </div>
    `;
}

function runLayout(layoutName) {
    if (!cy) return;
    cy.layout({ name: layoutName, animate: true, animationDuration: 500 }).run();
}
