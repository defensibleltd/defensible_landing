// Dashboard data
const dashboardData = {
  "overall_score": {
    "current": 75.12,
    "maximum": 110,
    "percentage": 68.3
  },
  "network_summary": {
    "ip_fabric_version": "7.3.17",
    "snapshot_b_uuid": "97ad7c58-341a-4e93-9612-8dd259d41672",
    "snapshot_a_uuid": "862778be-0d98-4013-806e-bd021f906ab6",
    "devices": {"old": 93, "new": 72, "delta": -21},
    "sites": {"old": 14, "new": 12, "delta": -2}
  },
  "controls": [
    {
      "id": 1,
      "name": "Inventory and Control of Enterprise Assets",
      "score": 9,
      "max_score": 10,
      "safeguards": ["1.1", "1.2", "1.3"],
      "detailed_safeguards": [
        {
          "id": "1.1",
          "name": "Establish and Maintain Detailed Enterprise Asset Inventory",
          "metrics": [
            {"label": "Network Devices", "old": 93, "new": 72, "delta": -21, "target": "N/A"},
            {"label": "Network Sites", "old": 14, "new": 12, "delta": -2, "target": "N/A"}
          ]
        },
        {
          "id": "1.2",
          "name": "Address Unauthorized Assets",
          "metrics": [
            {"label": "Discovery Issues", "old": 5, "new": 2, "delta": -3, "target": "≤0"}
          ]
        },
        {
          "id": "1.3",
          "name": "Utilize an Active Discovery Tool",
          "metrics": [
            {"label": "Intent Checks", "old": 167, "new": 167, "delta": 0, "target": "≥0"}
          ]
        }
      ]
    },
    {
      "id": 2,
      "name": "Inventory and Control of Software Assets",
      "score": 9.92,
      "max_score": 10,
      "safeguards": ["2.1", "2.2", "2.4"],
      "detailed_safeguards": [
        {
          "id": "2.1 & 2.4",
          "name": "Establish and Maintain Software Inventory / Utilize Automated Tools",
          "metrics": [
            {"label": "Platform Types", "old": 15, "new": 15, "delta": 0, "target": "≤0"},
            {"label": "Highest NOS Version Variance", "old": "8 Cisco IOS", "new": "5 Arista EOS", "delta": -3, "target": "3"}
          ]
        },
        {
          "id": "2.2",
          "name": "Software Lifecycle Management",
          "metrics": [
            {"label": "End of Support Devices", "old": "1%", "new": "2%", "delta": "+1%", "target": "0%"}
          ]
        }
      ]
    },
    {
      "id": 3,
      "name": "Data Protection",
      "score": 7.25,
      "max_score": 10,
      "safeguards": ["3.3", "3.8", "3.10", "3.14"],
      "detailed_safeguards": [
        {
          "id": "3.3",
          "name": "Configure Data Access Control Lists",
          "metrics": [
            {"label": "ANY/ANY ACL Policies", "old": 18, "new": 17, "delta": -1, "target": "≤0"}
          ]
        },
        {
          "id": "3.8",
          "name": "Document Data Flows",
          "metrics": [
            {"label": "Devices in DNS", "old": "86%", "new": "84%", "delta": "-2%", "target": "100%"}
          ]
        },
        {
          "id": "3.10",
          "name": "Encrypt Sensitive Data in Transit",
          "metrics": [
            {"label": "Telnet Enabled", "old": "4%", "new": "3%", "delta": "-1%", "target": "0%"}
          ]
        },
        {
          "id": "3.14",
          "name": "Log Sensitive Data Access",
          "metrics": [
            {"label": "Remote Logging", "old": "59%", "new": "59%", "delta": "0%", "target": "100%"},
            {"label": "TACACS/RADIUS", "old": "47%", "new": "40%", "delta": "-7%", "target": "≥0"}
          ]
        }
      ]
    },
    {
      "id": 4,
      "name": "Secure Configuration of Enterprise Assets and Software",
      "score": 7.96,
      "max_score": 10,
      "safeguards": ["4.6", "4.7", "4.9"],
      "detailed_safeguards": [
        {
          "id": "4.6",
          "name": "Securely Manage Enterprise Assets and Software",
          "metrics": [
            {"label": "Telnet Enabled", "old": "4%", "new": "3%", "delta": "-1%", "target": "0%"}
          ]
        },
        {
          "id": "4.7",
          "name": "Manage Default Accounts on Enterprise Assets and Software",
          "metrics": [
            {"label": "Local User Accounts", "old": "52%", "new": "52%", "delta": "0%", "target": "N/A"}
          ]
        },
        {
          "id": "4.9",
          "name": "Configure Trusted DNS Servers on Enterprise Assets",
          "metrics": [
            {"label": "DNS Resolvers", "old": 125, "new": 130, "delta": +5, "target": "≥0"}
          ]
        }
      ]
    },
    {
      "id": 5,
      "name": "Account Management",
      "score": 4.08,
      "max_score": 10,
      "safeguards": ["5.1", "5.4"],
      "detailed_safeguards": [
        {
          "id": "5.1",
          "name": "Manage Default Accounts on Enterprise Assets and Software",
          "metrics": [
            {"label": "Local User Accounts", "old": "52%", "new": "52%", "delta": "0%", "target": "100%"}
          ]
        },
        {
          "id": "5.4",
          "name": "Restrict Administrator Privileges to Dedicated Administrator Accounts",
          "metrics": [
            {"label": "TACACS/RADIUS", "old": "47%", "new": "40%", "delta": "-7%", "target": "≥0"}
          ]
        }
      ]
    },
    {
      "id": 6,
      "name": "Access Control Management",
      "score": 4,
      "max_score": 10,
      "safeguards": ["6.6", "6.7"],
      "detailed_safeguards": [
        {
          "id": "6.6 & 6.7",
          "name": "Establish Authentication Inventory / Centralize Access Control",
          "metrics": [
            {"label": "TACACS/RADIUS", "old": "47%", "new": "40%", "delta": "-7%", "target": "≥0"}
          ]
        }
      ]
    },
    {
      "id": 8,
      "name": "Audit Log Management",
      "score": 7.36,
      "max_score": 10,
      "safeguards": ["8.2", "8.4"],
      "detailed_safeguards": [
        {
          "id": "8.2",
          "name": "Collect Audit Logs",
          "metrics": [
            {"label": "Local Logging", "old": "82%", "new": "85%", "delta": "+3%", "target": "100%"},
            {"label": "Remote Logging", "old": "59%", "new": "59%", "delta": "0%", "target": "100%"}
          ]
        },
        {
          "id": "8.4",
          "name": "Standardize Time Synchronization",
          "metrics": [
            {"label": "NTP Configured", "old": "63%", "new": "65%", "delta": "+2%", "target": "100%"}
          ]
        }
      ]
    },
    {
      "id": 12,
      "name": "Network Infrastructure Management",
      "score": 8.7,
      "max_score": 10,
      "safeguards": ["12.1", "12.2", "12.3", "12.4", "12.5"],
      "detailed_safeguards": [
        {
          "id": "12.1",
          "name": "Ensure Network Infrastructure is Kept Up-to-Date",
          "metrics": [
            {"label": "End of Support", "old": "1%", "new": "2%", "delta": "+1%", "target": "0%"}
          ]
        },
        {
          "id": "12.2",
          "name": "Establish and Maintain a Secure Network Architecture",
          "metrics": [
            {"label": "Zone Firewall Policies", "old": 253, "new": 250, "delta": -3, "target": "≥0"}
          ]
        },
        {
          "id": "12.3",
          "name": "Securely Manage Network Infrastructure",
          "metrics": [
            {"label": "Telnet Enabled", "old": "4%", "new": "3%", "delta": "-1%", "target": "0%"}
          ]
        },
        {
          "id": "12.4",
          "name": "Establish and Maintain Architecture Diagrams",
          "metrics": [
            {"label": "Site Diagrams", "old": 14, "new": 12, "delta": -2, "target": "N/A"}
          ]
        },
        {
          "id": "12.5",
          "name": "Centralize Network Authentication, Authorization, and Auditing (AAA)",
          "metrics": [
            {"label": "TACACS/RADIUS", "old": "47%", "new": "40%", "delta": "-7%", "target": "≥0"}
          ]
        }
      ]
    },
    {
      "id": 13,
      "name": "Network Monitoring and Defence",
      "score": 7.1,
      "max_score": 10,
      "safeguards": ["13.4", "13.6", "13.9"],
      "detailed_safeguards": [
        {
          "id": "13.4",
          "name": "Perform Traffic Filtering Between Network Segments",
          "metrics": [
            {"label": "Zone Firewall Policies", "old": 253, "new": 250, "delta": -3, "target": "≥0"},
            {"label": "ANY/ANY ACL Policies", "old": 18, "new": 17, "delta": -1, "target": "≤0"}
          ]
        },
        {
          "id": "13.6",
          "name": "Collect Network Traffic Flow Logs",
          "metrics": [
            {"label": "NetFlow/IPFIX Devices", "old": 26, "new": 27, "delta": +1, "target": "≥0"}
          ]
        },
        {
          "id": "13.9",
          "name": "Deploy Port-Level Access Control",
          "metrics": [
            {"label": "802.1x Enabled", "old": "32%", "new": "40%", "delta": "+8%", "target": "100%"}
          ]
        }
      ]
    },
    {
      "id": 17,
      "name": "Incident Response Management",
      "score": 4,
      "max_score": 10,
      "safeguards": ["17.9"],
      "detailed_safeguards": [
        {
          "id": "17.9",
          "name": "Establish and Maintain Security Incident Thresholds",
          "metrics": [
            {"label": "IPv4 Routes", "old": 2367, "new": 1557, "delta": -810, "target": "≥0"},
            {"label": "Unstable Routes", "old": 32, "new": 15, "delta": -17, "target": "0"},
            {"label": "ErrDisabled Interfaces", "old": "1%", "new": "0%", "delta": "-1%", "target": "0%"}
          ]
        }
      ]
    },
    {
      "id": 18,
      "name": "Penetration Testing",
      "score": 5.75,
      "max_score": 10,
      "safeguards": ["18.4"],
      "detailed_safeguards": [
        {
          "id": "18.4",
          "name": "Validate Security Measures",
          "metrics": [
            {"label": "Zone Firewall Policies", "old": 253, "new": 250, "delta": -3, "target": "≥0"},
            {"label": "ANY/ANY ACL Policies", "old": 18, "new": 17, "delta": -1, "target": "≤0"}
          ]
        }
      ]
    }
  ]
};

// Chart colors from design system
const chartColors = ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F', '#DB4545', '#D2BA4C', '#964325', '#944454', '#13343B'];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeHeroSection();
    renderControlsGrid();
    renderDetailedMetrics();
    initializeCharts();
    populateMetricsTable();
    setupModalHandlers();
    animateElements();
});

function initializeHeroSection() {
    // Animate circle progress
    const circleProgress = document.querySelector('.circle-progress');
    const percentage = dashboardData.overall_score.percentage;
    
    setTimeout(() => {
        circleProgress.style.setProperty('--percentage', percentage);
    }, 500);

    // Animate score numbers
    animateNumber('.score-number', 0, dashboardData.overall_score.current, 2000);
}

function renderControlsGrid() {
    const grid = document.getElementById('controlsGrid');
    
    dashboardData.controls.forEach((control, index) => {
        const card = createControlCard(control);
        card.classList.add('slide-up');
        card.style.animationDelay = `${index * 100}ms`;
        grid.appendChild(card);
    });
}

function createControlCard(control) {
    const card = document.createElement('div');
    card.className = 'control-card';
    card.dataset.controlId = control.id;
    
    const percentage = (control.score / control.max_score) * 100;
    const progressClass = getProgressClass(percentage);
    const safeguardsText = control.safeguards.join(', ');
    
    // Get first few metrics for quick display
    const displayMetrics = control.detailed_safeguards.flatMap(sg => sg.metrics).slice(0, 3);
    
    card.innerHTML = `
        <div class="control-header">
            <div class="control-number">${control.id}</div>
            <div class="control-score">
                <span class="score-value">${control.score}</span>
                <span class="score-max">/ ${control.max_score}</span>
            </div>
        </div>
        <h3 class="control-name">${control.name}</h3>
        <div class="control-safeguards">Safeguards: ${safeguardsText}</div>
        <div class="control-progress">
            <div class="progress-fill ${progressClass}" style="width: ${percentage}%"></div>
        </div>
        <div class="control-metrics">
            ${displayMetrics.map(metric => `
                <div class="metric-item">
                    <span class="metric-label">${metric.label}</span>
                    <span class="metric-value">${metric.new}</span>
                </div>
            `).join('')}
        </div>
    `;
    
    card.addEventListener('click', () => showControlModal(control));
    
    return card;
}

function renderDetailedMetrics() {
    const container = document.getElementById('detailedMetrics');
    
    dashboardData.controls.forEach((control, index) => {
        const detailedCard = createDetailedControlCard(control);
        detailedCard.classList.add('slide-up');
        detailedCard.style.animationDelay = `${index * 50}ms`;
        container.appendChild(detailedCard);
    });
}

function createDetailedControlCard(control) {
    const card = document.createElement('div');
    card.className = 'detailed-control';
    card.dataset.controlId = control.id;
    
    const percentage = (control.score / control.max_score) * 100;
    
    card.innerHTML = `
        <div class="detailed-control-header">
            <div class="detailed-control-title">
                <div class="detailed-control-number">${control.id}</div>
                <div class="detailed-control-info">
                    <h3>${control.name}</h3>
                    <div class="detailed-control-score">Safeguards: ${control.safeguards.join(', ')}</div>
                </div>
            </div>
            <div class="detailed-control-overall-score">
                <span class="detailed-score-value">${control.score}</span>
                <span class="detailed-score-max">/ ${control.max_score}</span>
                <div class="expand-icon">▼</div>
            </div>
        </div>
        <div class="detailed-control-content">
            <div class="safeguards-list">
                ${control.detailed_safeguards.map(safeguard => createSafeguardItem(safeguard)).join('')}
            </div>
        </div>
    `;
    
    // Add click handler for expand/collapse
    const header = card.querySelector('.detailed-control-header');
    header.addEventListener('click', () => {
        card.classList.toggle('expanded');
    });
    
    return card;
}

function createSafeguardItem(safeguard) {
    return `
        <div class="safeguard-item">
            <div class="safeguard-header">
                <div class="safeguard-id">${safeguard.id}</div>
                <div class="safeguard-name">${safeguard.name}</div>
            </div>
            <div class="safeguard-metrics">
                ${safeguard.metrics.map(metric => createSafeguardMetric(metric)).join('')}
            </div>
        </div>
    `;
}

function createSafeguardMetric(metric) {
    const deltaClass = getChangeClass(metric.delta);
    const deltaText = formatDelta(metric.delta);
    
    return `
        <div class="safeguard-metric">
            <div class="metric-name">${metric.label}</div>
            <div class="metric-change">
                <span class="metric-old">${metric.old}</span>
                <span>→</span>
                <span class="metric-new">${metric.new}</span>
            </div>
            <div class="metric-delta ${deltaClass}">${deltaText}</div>
            <div class="metric-target">Target: ${metric.target}</div>
        </div>
    `;
}

function getProgressClass(percentage) {
    if (percentage >= 90) return 'progress-excellent';
    if (percentage >= 70) return 'progress-good';
    if (percentage >= 50) return 'progress-moderate';
    return 'progress-poor';
}

function initializeCharts() {
    createScoreChart();
    createNetworkChart();
    createSecurityChart();
}

function createScoreChart() {
    const ctx = document.getElementById('scoreChart').getContext('2d');
    
    const scoreRanges = {
        'Excellent (9-10)': 0,
        'Good (7-9)': 0,
        'Moderate (5-7)': 0,
        'Poor (0-5)': 0
    };
    
    dashboardData.controls.forEach(control => {
        const score = control.score;
        if (score >= 9) scoreRanges['Excellent (9-10)']++;
        else if (score >= 7) scoreRanges['Good (7-9)']++;
        else if (score >= 5) scoreRanges['Moderate (5-7)']++;
        else scoreRanges['Poor (0-5)']++;
    });
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(scoreRanges),
            datasets: [{
                data: Object.values(scoreRanges),
                backgroundColor: chartColors.slice(0, 4),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function createNetworkChart() {
    const ctx = document.getElementById('networkChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Devices', 'Sites', 'Discovery Issues'],
            datasets: [
                {
                    label: 'Previous',
                    data: [93, 14, 5],
                    backgroundColor: chartColors[1]
                },
                {
                    label: 'Current',
                    data: [72, 12, 2],
                    backgroundColor: chartColors[0]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    position: 'top'
                }
            }
        }
    });
}

function createSecurityChart() {
    const ctx = document.getElementById('securityChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Assets', 'Software', 'Data Protection', 'Configuration', 'Access Control', 'Monitoring'],
            datasets: [{
                label: 'Security Score',
                data: [9, 9.92, 7.25, 7.96, 4, 7.1],
                backgroundColor: 'rgba(31, 184, 205, 0.2)',
                borderColor: chartColors[0],
                borderWidth: 2,
                pointBackgroundColor: chartColors[0]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 10
                }
            }
        }
    });
}

function populateMetricsTable() {
    const tableBody = document.querySelector('#metricsTable tbody');
    
    dashboardData.controls.forEach(control => {
        const primaryMetric = control.detailed_safeguards[0].metrics[0];
        const row = document.createElement('tr');
        
        const changeClass = getChangeClass(primaryMetric.delta);
        const changeText = formatDelta(primaryMetric.delta);
        
        row.innerHTML = `
            <td>Control ${control.id}</td>
            <td><strong>${control.score}</strong>/${control.max_score}</td>
            <td>${primaryMetric.label}</td>
            <td>${primaryMetric.old}</td>
            <td>${primaryMetric.new}</td>
            <td class="${changeClass}">${changeText}</td>
            <td>${primaryMetric.target}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

function getChangeClass(delta) {
    if (typeof delta === 'string') {
        if (delta.includes('+')) return 'positive';
        if (delta.includes('-')) return 'negative';
        return 'neutral';
    }
    
    if (delta > 0) return 'positive';
    if (delta < 0) return 'negative';
    return 'neutral';
}

function formatDelta(delta) {
    if (typeof delta === 'string') return delta;
    if (delta === 0) return '0';
    return delta > 0 ? `+${delta}` : `${delta}`;
}

function showControlModal(control) {
    const modal = document.getElementById('controlModal');
    const title = document.getElementById('modalTitle');
    const body = document.getElementById('modalBody');
    
    title.textContent = `Control ${control.id}: ${control.name}`;
    
    body.innerHTML = `
        <div class="modal-score" style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: var(--color-primary);">${control.score} / ${control.max_score}</h2>
            <p>Current Score</p>
            <p style="color: var(--color-text-secondary); font-size: var(--font-size-sm);">
                Safeguards: ${control.safeguards.join(', ')}
            </p>
        </div>
        <h4>Detailed Metrics by Safeguard:</h4>
        ${control.detailed_safeguards.map(safeguard => `
            <div style="margin-bottom: 20px; padding: 16px; background: var(--color-background); border-radius: var(--radius-base);">
                <h5 style="color: var(--color-primary); margin-bottom: 12px;">
                    ${safeguard.id}: ${safeguard.name}
                </h5>
                ${safeguard.metrics.map(metric => `
                    <div class="modal-metric">
                        <div>
                            <strong>${metric.label}</strong><br>
                            <small>Target: ${metric.target}</small>
                        </div>
                        <div style="text-align: right;">
                            <div>${metric.old} → ${metric.new}</div>
                            <div class="${getChangeClass(metric.delta)}" style="font-size: 0.9em;">
                                ${formatDelta(metric.delta)}
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `).join('')}
    `;
    
    modal.classList.remove('hidden');
    // Prevent body scroll when modal is open
    document.body.style.overflow = 'hidden';
}

function hideModal() {
    const modal = document.getElementById('controlModal');
    modal.classList.add('hidden');
    // Restore body scroll
    document.body.style.overflow = '';
    
    // Clear modal content to prevent any leftover elements
    const title = document.getElementById('modalTitle');
    const body = document.getElementById('modalBody');
    title.textContent = '';
    body.innerHTML = '';
}

function setupModalHandlers() {
    const modal = document.getElementById('controlModal');
    const closeBtn = document.getElementById('modalClose');
    const backdrop = modal.querySelector('.modal-backdrop');
    
    closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        hideModal();
    });
    
    backdrop.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        hideModal();
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
            e.preventDefault();
            hideModal();
        }
    });
    
    // Prevent modal content clicks from closing modal
    modal.querySelector('.modal-content').addEventListener('click', (e) => {
        e.stopPropagation();
    });
}

function animateNumber(selector, start, end, duration) {
    const element = document.querySelector(selector);
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = start + (end - start) * easeOutCubic(progress);
        element.textContent = current.toFixed(2);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
}

function animateElements() {
    // Add intersection observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, { threshold: 0.1 });
    
    // Observe all major sections
    document.querySelectorAll('.chart-card, .stat-card, .detailed-control').forEach(el => {
        observer.observe(el);
    });
}