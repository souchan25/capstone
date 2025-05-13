document.addEventListener('DOMContentLoaded', function() {
    // Add Font Awesome for icons
    const fontAwesomeLink = document.createElement('link');
    fontAwesomeLink.rel = 'stylesheet';
    fontAwesomeLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css';
    document.head.appendChild(fontAwesomeLink);
    
    // Add current date to dashboard
    addCurrentDate();

    // Load dashboard data via AJAX
    fetchDashboardData();
    
    // Add event listeners for any interactive elements
    setupEventListeners();
});

function addCurrentDate() {
    const dateDisplay = document.querySelector('.date-display');
    if (dateDisplay) {
        const now = new Date();
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateDisplay.textContent = now.toLocaleDateString(undefined, options);
    }
}

function setupEventListeners() {
    // Example: Toggle visibility of medical info card
    const infoCardHeader = document.querySelector('.medical-info-card h3');
    const statusIndicators = document.querySelector('.status-indicators');
    
    if (infoCardHeader && statusIndicators) {
        infoCardHeader.addEventListener('click', function() {
            statusIndicators.classList.toggle('collapsed');
            infoCardHeader.classList.toggle('collapsed');
        });
    }
}

function fetchDashboardData() {
    // Show loading indicators
    document.querySelectorAll('.stat-value').forEach(el => {
        el.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    });
    
    // Fetch real data from API
    fetch('/api/admin/dashboard-stats/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update dashboard stats
            updateDashboardStats(data.counts);
            
            // Initialize charts with API data
            initializeCharts(data.charts);
        })
        .catch(error => {
            console.error('Error fetching dashboard data:', error);
            // Fall back to sample data
            updateDashboardStats({
                'total_reports': 156,
                'total_students': 1243,
                'today_reports': 12,
                'high_severity': 5
            });
            
            // Initialize charts with sample data
            initializeChartsWithSampleData();
        });
}

function updateDashboardStats(counts) {
    // Update stats with animated counting
    animateCount('total-reports', 0, counts.total_reports, 1000);
    animateCount('active-students', 0, counts.total_students, 1500);
    animateCount('today-reports', 0, counts.today_reports, 800);
    animateCount('high-severity', 0, counts.high_severity, 600);
}

function animateCount(elementId, start, end, duration) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value.toLocaleString();
        
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    
    window.requestAnimationFrame(step);
}

function initializeCharts(chartData) {
    // Symptom Chart with real data
    if (document.getElementById('symptomChart') && chartData.symptoms) {
        const symptomCtx = document.getElementById('symptomChart').getContext('2d');
        const symptomData = {
            labels: chartData.symptoms.labels,
            datasets: [{
                label: 'Number of Reports',
                data: chartData.symptoms.data,
                backgroundColor: generateGreenColorScale(chartData.symptoms.labels.length),
                borderWidth: 1
            }]
        };
        
        createBarChart(symptomCtx, symptomData);
    }
    
    // Severity Chart with real data
    if (document.getElementById('severityChart') && chartData.severity) {
        const severityCtx = document.getElementById('severityChart').getContext('2d');
        const severityData = {
            labels: chartData.severity.labels,
            datasets: [{
                label: 'Reports by Severity',
                data: chartData.severity.data,
                backgroundColor: getSeverityColors(chartData.severity.labels),
                borderWidth: 1
            }]
        };
        
        createDoughnutChart(severityCtx, severityData);
    }
    
    // Weekly Trend Chart
    if (document.getElementById('trendChart')) {
        createWeeklyTrendChart();
    }
    
    // Common Conditions Chart
    if (document.getElementById('conditionsChart')) {
        createConditionsChart();
    }
}

function initializeChartsWithSampleData() {
    // Sample data as fallback
    const symptomData = {
        labels: ['Headache', 'Fever', 'Cough', 'Sore Throat', 'Fatigue', 'Other'],
        datasets: [{
            label: 'Number of Reports',
            data: [45, 32, 28, 19, 15, 17],
            backgroundColor: generateGreenColorScale(6),
            borderWidth: 1
        }]
    };
    
    const severityData = {
        labels: ['LOW', 'MEDIUM', 'HIGH'],
        datasets: [{
            label: 'Reports by Severity',
            data: [87, 64, 5],
            backgroundColor: getSeverityColors(['LOW', 'MEDIUM', 'HIGH']),
            borderWidth: 1
        }]
    };
    
    // Symptom Chart
    if (document.getElementById('symptomChart')) {
        const symptomCtx = document.getElementById('symptomChart').getContext('2d');
        createBarChart(symptomCtx, symptomData);
    }
    
    // Severity Chart
    if (document.getElementById('severityChart')) {
        const severityCtx = document.getElementById('severityChart').getContext('2d');
        createDoughnutChart(severityCtx, severityData);
    }
    
    // Weekly Trend Chart
    if (document.getElementById('trendChart')) {
        createWeeklyTrendChart();
    }
    
    // Common Conditions Chart
    if (document.getElementById('conditionsChart')) {
        createConditionsChart();
    }
}

function createWeeklyTrendChart() {
    const ctx = document.getElementById('trendChart').getContext('2d');
    
    // Generate dates for the last 7 days
    const dates = [];
    for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        dates.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
    }
    
    const data = {
        labels: dates,
        datasets: [
            {
                label: 'Reports',
                data: [8, 12, 9, 14, 23, 10, 12],
                borderColor: '#0073cf',
                backgroundColor: 'rgba(0, 115, 207, 0.1)',
                tension: 0.4,
                fill: true
            },
            {
                label: 'Resolved Cases',
                data: [5, 9, 7, 10, 15, 8, 7],
                borderColor: '#5cb85c',
                backgroundColor: 'rgba(92, 184, 92, 0.1)',
                tension: 0.4,
                fill: true
            }
        ]
    };
    
    new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Cases'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    });
}

function createConditionsChart() {
    const ctx = document.getElementById('conditionsChart').getContext('2d');
    
    const data = {
        labels: ['Respiratory', 'Gastrointestinal', 'Dermatological', 'ENT', 'Viral', 'Other'],
        datasets: [{
            label: 'Frequency',
            data: [35, 20, 15, 12, 28, 10],
            backgroundColor: [
                '#0073cf',
                '#5cb85c',
                '#f0ad4e',
                '#d9534f',
                '#5bc0de',
                '#777777'
            ],
            borderWidth: 1
        }]
    };
    
    new Chart(ctx, {
        type: 'polarArea',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw} cases`;
                        }
                    }
                }
            }
        }
    });
}

function createBarChart(ctx, data) {
    return new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Reports'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Symptoms'
                    }
                }
            }
        }
    });
}

function createDoughnutChart(ctx, data) {
    return new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.formattedValue;
                            const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((context.raw / total) * 100);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            },
            cutout: '60%'
        }
    });
}

function generateGreenColorScale(count) {
    const colors = [];
    // Start with primary CPSU green and gradually lighten
    const startColor = [0, 100, 0]; // rgb(0, 100, 0) - dark green
    const endColor = [204, 204, 0];  // rgb(204, 204, 0) - CPSU yellow-green
    
    for (let i = 0; i < count; i++) {
        const ratio = i / (count - 1 || 1); // Avoid division by zero
        const r = Math.round(startColor[0] + ratio * (endColor[0] - startColor[0]));
        const g = Math.round(startColor[1] + ratio * (endColor[1] - startColor[1]));
        const b = Math.round(startColor[2] + ratio * (endColor[2] - startColor[2]));
        colors.push(`rgb(${r}, ${g}, ${b})`);
    }
    
    return colors;
}

function getSeverityColors(labels) {
    return labels.map(label => {
        switch(label.toUpperCase()) {
            case 'LOW': return '#8BC34A';
            case 'MEDIUM': return '#FFC107';
            case 'HIGH': return '#F44336';
            default: return '#999999';
        }
    });
}

// In a production environment, you would implement API calls like this:
// function fetchDataFromAPI(endpoint) {
//     return fetch(`/api/${endpoint}/`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         });
// } 