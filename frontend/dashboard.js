async function fetchJSON(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Failed to fetch ${path}`);
  }
  return response.json();
}

function renderIssues(issues) {
  const container = document.getElementById('issues');
  container.innerHTML = '';
  issues.forEach((issue) => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `<strong>${issue.issue_type}</strong> - ${issue.severity}<br/>Resource: ${issue.resource.name}`;
    container.appendChild(card);
  });
}

function renderCompliance(data) {
  const container = document.getElementById('compliance');
  container.innerHTML = `<p>Risk Score: ${data.risk_score}</p>`;
  Object.entries(data.mapping).forEach(([framework, controls]) => {
    const row = document.createElement('div');
    row.className = 'card';
    row.innerHTML = `<strong>${framework}</strong>: ${controls.join(', ') || 'No controls triggered'}`;
    container.appendChild(row);
  });
}

function renderFix(plan) {
  const container = document.getElementById('fix');
  container.textContent = plan?.content || 'No fix generated yet';
}

async function loadDashboard() {
  try {
    const issues = await fetchJSON('/issues');
    renderIssues(issues);
    const compliance = await fetchJSON('/compliance');
    renderCompliance(compliance);
    const fix = await fetchJSON('/fix/latest');
    renderFix(fix);
  } catch (error) {
    console.error(error);
  }
}

window.addEventListener('DOMContentLoaded', loadDashboard);
