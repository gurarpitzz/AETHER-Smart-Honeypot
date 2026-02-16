let chart;
const maxDataPoints = 20;

document.addEventListener('DOMContentLoaded', () => {
    initChart();
    setInterval(fetchUpdate, 2000); // 2s Tick
});

function initChart() {
    const ctx = document.getElementById('metricsChart').getContext('2d');

    // Gradient for the chart
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(255, 153, 0, 0.5)');
    gradient.addColorStop(1, 'rgba(255, 153, 0, 0)');

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Adversary Confusion Index',
                data: [],
                borderColor: '#ff9900',
                backgroundColor: gradient,
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointRadius: 0
            },
            {
                label: 'Risk Score (x10)',
                data: [],
                borderColor: '#ff3333',
                borderWidth: 1,
                borderDash: [5, 5],
                tension: 0.1,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 500 },
            scales: {
                x: { display: false },
                y: {
                    grid: { color: '#332200' },
                    ticks: { color: '#885500' }
                }
            },
            plugins: {
                legend: { labels: { color: '#ff9900', font: { family: 'Courier New' } } }
            }
        }
    });
}

function fetchUpdate() {
    fetch('/api/step')
        .then(response => response.json())
        .then(data => {
            updateDashboard(data);
        })
        .catch(err => console.error("Connection Lost", err));
}

function updateDashboard(data) {
    // 1. Text Metrics
    document.getElementById('source-ip').innerText = data.attacker.ip;
    document.getElementById('risk-score').innerText = data.attacker.behavior_score.toFixed(2);

    document.getElementById('conf-index').innerText = data.defense.metrics.adversary_confusion_index.toFixed(1);
    document.getElementById('active-decoys').innerText = data.defense.metrics.active_deceptions;

    const defenseActionBox = document.getElementById('defense-action');
    defenseActionBox.innerText = `TYPE: ${data.defense.action}\nDATA: ${data.defense.content.substring(0, 40)}...`;

    // 2. Chart Update
    const stepLabel = `T-${data.step}`;
    addData(chart, stepLabel, [
        data.defense.metrics.adversary_confusion_index,
        data.attacker.behavior_score * 10 // Scale up for visibility
    ]);

    // 3. Log Stream
    const logContainer = document.getElementById('log-terminal');
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    if (data.attacker.behavior_score > 0.7) {
        entry.classList.add('high-risk');
    }
    entry.innerText = data.log_message;
    logContainer.prepend(entry);

    if (logContainer.children.length > 20) logContainer.lastChild.remove();
}

function addData(chart, label, dataPoints) {
    chart.data.labels.push(label);

    chart.data.datasets.forEach((dataset, i) => {
        dataset.data.push(dataPoints[i]);
    });

    if (chart.data.labels.length > maxDataPoints) {
        chart.data.labels.shift();
        chart.data.datasets.forEach((dataset) => {
            dataset.data.shift();
        });
    }
    chart.update();
}
