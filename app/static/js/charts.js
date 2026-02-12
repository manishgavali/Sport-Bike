/* ============================================
   CHART.JS INTEGRATION FOR ANALYTICS
   Bike performance, maintenance, and riding analytics
   ============================================ */

// Chart.js default configuration
Chart.defaults.color = '#a0a5b8';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";

// Custom color schemes
const chartColors = {
    primary: '#00d9ff',
    secondary: '#4169e1',
    accent: '#ff6b35',
    success: '#4caf50',
    warning: '#ffc107',
    danger: '#f44336',
    gradient: {
        cyan: ['rgba(0, 217, 255, 0.8)', 'rgba(0, 217, 255, 0.2)'],
        blue: ['rgba(65, 105, 225, 0.8)', 'rgba(65, 105, 225, 0.2)'],
        orange: ['rgba(255, 107, 53, 0.8)', 'rgba(255, 107, 53, 0.2)']
    }
};

/**
 * Create gradient for chart
 */
function createGradient(ctx, colors) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, colors[0]);
    gradient.addColorStop(1, colors[1]);
    return gradient;
}

/**
 * Bike Performance Comparison Chart
 */
function createPerformanceComparisonChart(canvasId, bikes, performanceData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const bikeNames = bikes.map(bike => `${bike.brand} ${bike.model}`);
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Power', 'Torque', 'Top Speed', 'Acceleration', 'Handling', 'Overall'],
            datasets: bikes.map((bike, index) => ({
                label: bikeNames[index],
                data: performanceData[index],
                backgroundColor: `rgba(${index * 80}, ${217 - index * 50}, 255, 0.2)`,
                borderColor: `rgba(${index * 80}, ${217 - index * 50}, 255, 1)`,
                borderWidth: 2,
                pointBackgroundColor: `rgba(${index * 80}, ${217 - index * 50}, 255, 1)`,
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: `rgba(${index * 80}, ${217 - index * 50}, 255, 1)`
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#ffffff',
                        padding: 20,
                        font: {
                            size: 14
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Performance Comparison',
                    color: '#00d9ff',
                    font: {
                        size: 18,
                        weight: 'bold'
                    },
                    padding: 20
                }
            },
            scales: {
                r: {
                    angleLines: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    pointLabels: {
                        color: '#a0a5b8',
                        font: {
                            size: 12
                        }
                    },
                    ticks: {
                        backdropColor: 'transparent',
                        color: '#a0a5b8'
                    }
                }
            }
        }
    });
}

/**
 * Mileage Comparison Bar Chart
 */
function createMileageComparisonChart(canvasId, bikes, mileageData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const bikeNames = bikes.map(bike => `${bike.brand} ${bike.model}`);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: bikeNames,
            datasets: [
                {
                    label: 'City Mileage',
                    data: mileageData.city,
                    backgroundColor: createGradient(ctx.getContext('2d'), chartColors.gradient.cyan),
                    borderColor: chartColors.primary,
                    borderWidth: 2,
                    borderRadius: 8
                },
                {
                    label: 'Highway Mileage',
                    data: mileageData.highway,
                    backgroundColor: createGradient(ctx.getContext('2d'), chartColors.gradient.blue),
                    borderColor: chartColors.secondary,
                    borderWidth: 2,
                    borderRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#ffffff',
                        padding: 20,
                        usePointStyle: true
                    }
                },
                title: {
                    display: true,
                    text: 'Mileage Comparison (km/l)',
                    color: '#00d9ff',
                    font: {
                        size: 18,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 31, 53, 0.9)',
                    borderColor: '#00d9ff',
                    borderWidth: 1,
                    titleColor: '#00d9ff',
                    bodyColor: '#ffffff',
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + ' km/l';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#a0a5b8',
                        callback: function(value) {
                            return value + ' km/l';
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#a0a5b8'
                    }
                }
            }
        }
    });
}

/**
 * Riding Analytics - Distance Over Time
 */
function createRidingDistanceChart(canvasId, dates, distances) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Distance (km)',
                data: distances,
                fill: true,
                backgroundColor: createGradient(ctx.getContext('2d'), chartColors.gradient.cyan),
                borderColor: chartColors.primary,
                borderWidth: 3,
                tension: 0.4,
                pointBackgroundColor: chartColors.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Riding Distance Over Time',
                    color: '#00d9ff',
                    font: {
                        size: 18,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 31, 53, 0.9)',
                    borderColor: '#00d9ff',
                    borderWidth: 1,
                    titleColor: '#00d9ff',
                    bodyColor: '#ffffff',
                    padding: 12
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#a0a5b8',
                        callback: function(value) {
                            return value + ' km';
                        }
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#a0a5b8'
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

/**
 * Maintenance Cost Breakdown Doughnut Chart
 */
function createMaintenanceCostChart(canvasId, costData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Engine Oil', 'Brake Pads', 'Tyres', 'Chain & Sprocket', 'Service', 'Others'],
            datasets: [{
                data: costData,
                backgroundColor: [
                    'rgba(0, 217, 255, 0.8)',
                    'rgba(65, 105, 225, 0.8)',
                    'rgba(255, 107, 53, 0.8)',
                    'rgba(76, 175, 80, 0.8)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(156, 39, 176, 0.8)'
                ],
                borderColor: [
                    '#00d9ff',
                    '#4169e1',
                    '#ff6b35',
                    '#4caf50',
                    '#ffc107',
                    '#9c27b0'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#ffffff',
                        padding: 15,
                        font: {
                            size: 13
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Maintenance Cost Breakdown',
                    color: '#00d9ff',
                    font: {
                        size: 18,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 31, 53, 0.9)',
                    borderColor: '#00d9ff',
                    borderWidth: 1,
                    titleColor: '#00d9ff',
                    bodyColor: '#ffffff',
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return label + ': ₹' + value.toLocaleString() + ' (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });
}

/**
 * Speed Distribution Chart
 */
function createSpeedDistributionChart(canvasId, speedRanges, frequencies) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: speedRanges,
            datasets: [{
                label: 'Frequency',
                data: frequencies,
                backgroundColor: createGradient(ctx.getContext('2d'), chartColors.gradient.orange),
                borderColor: chartColors.accent,
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Speed Distribution',
                    color: '#00d9ff',
                    font: {
                        size: 18,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#a0a5b8'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#a0a5b8'
                    }
                }
            }
        }
    });
}

/**
 * Road Type Usage Pie Chart
 */
function createRoadTypeChart(canvasId, roadTypes) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['City', 'Highway', 'Track'],
            datasets: [{
                data: roadTypes,
                backgroundColor: [
                    'rgba(0, 217, 255, 0.8)',
                    'rgba(255, 107, 53, 0.8)',
                    'rgba(76, 175, 80, 0.8)'
                ],
                borderColor: [
                    '#00d9ff',
                    '#ff6b35',
                    '#4caf50'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#ffffff',
                        padding: 15,
                        font: {
                            size: 13
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Road Type Usage',
                    color: '#00d9ff',
                    font: {
                        size: 18,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 31, 53, 0.9)',
                    borderColor: '#00d9ff',
                    borderWidth: 1,
                    titleColor: '#00d9ff',
                    bodyColor: '#ffffff',
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return label + ': ' + value + ' rides (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });
}

/**
 * Fuel Consumption Trend Chart
 */
function createFuelConsumptionChart(canvasId, months, consumption) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'Fuel Consumption (L)',
                data: consumption,
                fill: true,
                backgroundColor: createGradient(ctx.getContext('2d'), chartColors.gradient.orange),
                borderColor: chartColors.accent,
                borderWidth: 3,
                tension: 0.4,
                pointBackgroundColor: chartColors.accent,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Monthly Fuel Consumption',
                    color: '#00d9ff',
                    font: {
                        size: 18,
                        weight: 'bold'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#a0a5b8',
                        callback: function(value) {
                            return value + ' L';
                        }
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#a0a5b8'
                    }
                }
            }
        }
    });
}

/**
 * Component Wear Progress Chart
 */
function createComponentWearChart(canvasId, components, wearLevels) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: components,
            datasets: [{
                label: 'Wear Level (%)',
                data: wearLevels,
                backgroundColor: wearLevels.map(wear => {
                    if (wear > 80) return 'rgba(244, 67, 54, 0.8)';
                    if (wear > 60) return 'rgba(255, 193, 7, 0.8)';
                    return 'rgba(76, 175, 80, 0.8)';
                }),
                borderColor: wearLevels.map(wear => {
                    if (wear > 80) return '#f44336';
                    if (wear > 60) return '#ffc107';
                    return '#4caf50';
                }),
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Component Wear Analysis',
                    color: '#00d9ff',
                    font: {
                        size: 18,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 31, 53, 0.9)',
                    borderColor: '#00d9ff',
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            return context.parsed.x + '% wear';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#a0a5b8',
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#a0a5b8'
                    }
                }
            }
        }
    });
}

/**
 * Initialize all charts on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.error('Chart.js library not loaded. Please include Chart.js in your HTML.');
        return;
    }

    // Auto-initialize charts based on data attributes
    const chartElements = document.querySelectorAll('[data-chart]');
    
    chartElements.forEach(element => {
        const chartType = element.dataset.chart;
        const chartData = JSON.parse(element.dataset.chartData || '{}');
        
        switch(chartType) {
            case 'performance':
                createPerformanceComparisonChart(element.id, chartData.bikes, chartData.performance);
                break;
            case 'mileage':
                createMileageComparisonChart(element.id, chartData.bikes, chartData.mileage);
                break;
            case 'distance':
                createRidingDistanceChart(element.id, chartData.dates, chartData.distances);
                break;
            case 'maintenance':
                createMaintenanceCostChart(element.id, chartData.costs);
                break;
            case 'speed':
                createSpeedDistributionChart(element.id, chartData.ranges, chartData.frequencies);
                break;
            case 'roadtype':
                createRoadTypeChart(element.id, chartData.types);
                break;
            case 'fuel':
                createFuelConsumptionChart(element.id, chartData.months, chartData.consumption);
                break;
            case 'wear':
                createComponentWearChart(element.id, chartData.components, chartData.wear);
                break;
        }
    });
});

// Export functions for external use
window.BikeCharts = {
    createPerformanceComparisonChart,
    createMileageComparisonChart,
    createRidingDistanceChart,
    createMaintenanceCostChart,
    createSpeedDistributionChart,
    createRoadTypeChart,
    createFuelConsumptionChart,
    createComponentWearChart
};
