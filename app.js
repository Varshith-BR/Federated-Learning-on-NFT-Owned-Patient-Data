// FL-NFT Healthcare System JavaScript

// Application data
const appData = {
    hospitals: [
        {"id": "metro_general", "name": "Metro General Hospital", "patients": 1283, "consented": 870, "consent_rate": 67.81},
        {"id": "regional_healthcare", "name": "Regional Healthcare System", "patients": 1268, "consented": 843, "consent_rate": 66.48},
        {"id": "veterans_affairs", "name": "Veterans Affairs Hospital", "patients": 1226, "consented": 878, "consent_rate": 71.62},
        {"id": "st_marys", "name": "St. Mary's Hospital", "patients": 1268, "consented": 858, "consent_rate": 67.67},
        {"id": "university_medical", "name": "University Medical Center", "patients": 1265, "consented": 877, "consent_rate": 69.33},
        {"id": "community_health", "name": "Community Health Network", "patients": 1234, "consented": 868, "consent_rate": 70.34},
        {"id": "city_medical", "name": "City Medical Center", "patients": 1231, "consented": 829, "consent_rate": 67.34},
        {"id": "childrens_medical", "name": "Children's Medical Center", "patients": 1225, "consented": 833, "consent_rate": 68.00}
    ],
    global_stats: {
        "total_patients": 10000,
        "total_consented": 6856,
        "overall_consent_rate": 68.56,
        "active_nodes": 8,
        "model_accuracy": 0.852,
        "training_rounds": 3
    },
    sample_patients: [
        {"id": "P000001", "age": 45, "gender": "Male", "condition": "Hypertension", "hospital": "Metro General Hospital", "wallet": "0x1a2b3c4d5e6f7890abcdef1234567890abcdef12", "consented": true, "consent_date": "2024-11-15", "expiry": "2025-11-15"},
        {"id": "P000002", "age": 32, "gender": "Female", "condition": "Diabetes", "hospital": "Regional Healthcare System", "wallet": "0x9876543210fedcba0987654321fedcba09876543", "consented": false, "consent_date": null, "expiry": null},
        {"id": "P000003", "age": 67, "gender": "Male", "condition": "Heart Disease", "hospital": "Veterans Affairs Hospital", "wallet": "0xabcdef1234567890abcdef1234567890abcdef12", "consented": true, "consent_date": "2024-10-20", "expiry": null},
        {"id": "P000004", "age": 28, "gender": "Female", "condition": "Asthma", "hospital": "St. Mary's Hospital", "wallet": "0x4567890abcdef1234567890abcdef1234567890", "consented": true, "consent_date": "2024-11-10", "expiry": "2025-11-10"},
        {"id": "P000005", "age": 55, "gender": "Male", "condition": "Arthritis", "hospital": "University Medical Center", "wallet": "0xfedcba0987654321fedcba0987654321fedcba09", "consented": false, "consent_date": null, "expiry": null}
    ],
    training_history: [
        {"round": 1, "accuracy": 0.864, "loss": 0.270, "nodes": 8, "data_points": 6856},
        {"round": 2, "accuracy": 0.835, "loss": 0.245, "nodes": 8, "data_points": 6856},
        {"round": 3, "accuracy": 0.852, "loss": 0.247, "nodes": 8, "data_points": 6856}
    ],
    blockchain_transactions: [
        {"hash": "0xabc123def456", "type": "NFT_MINT", "patient": "P000001", "timestamp": "2024-11-15 10:30:00", "status": "confirmed"},
        {"hash": "0xdef456ghi789", "type": "CONSENT_UPDATE", "patient": "P000002", "timestamp": "2024-11-15 11:45:00", "status": "confirmed"},
        {"hash": "0x789abcdef012", "type": "FL_TRAINING", "round": 3, "timestamp": "2024-11-15 12:00:00", "status": "confirmed"},
        {"hash": "0x012345abc678", "type": "NFT_MINT", "patient": "P000004", "timestamp": "2024-11-14 09:15:00", "status": "confirmed"},
        {"hash": "0x678def901234", "type": "CONSENT_REVOKE", "patient": "P000005", "timestamp": "2024-11-14 14:20:00", "status": "confirmed"}
    ]
};

// Global variables
let trainingInterval = null;
let currentTrainingRound = 0;
let charts = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing application...');
    
    // Wait a moment for all elements to be properly rendered
    setTimeout(() => {
        initializeNavigation();
        loadOverviewData();
        loadPatientPortal();
        loadHospitalDashboard();
        loadBlockchainData();
        
        // Initialize charts after another short delay
        setTimeout(initializeCharts, 200);
    }, 100);
});

// Navigation functionality - Fixed version
function initializeNavigation() {
    console.log('Initializing navigation...');
    
    // Get all navigation links and sections
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');
    
    console.log('Found nav links:', navLinks.length);
    console.log('Found sections:', sections.length);
    
    // Add click handlers to navigation links
    navLinks.forEach((link, index) => {
        console.log(`Setting up nav link ${index}:`, link.getAttribute('href'));
        
        link.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const targetId = this.getAttribute('href').substring(1);
            console.log('Navigation clicked, target:', targetId);
            
            // Remove active class from all nav links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Hide all sections first
            sections.forEach(section => {
                section.style.display = 'none';
                section.classList.remove('active');
            });
            
            // Show target section
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.style.display = 'block';
                targetSection.classList.add('active');
                console.log('Section shown successfully:', targetId);
                
                // Initialize charts for specific sections
                setTimeout(() => {
                    if (targetId === 'hospital-dashboard' || targetId === 'fl-demo' || targetId === 'analytics') {
                        initializeCharts();
                    }
                }, 100);
            } else {
                console.error('Section not found:', targetId);
            }
        });
    });
    
    // Show overview section by default
    showSection('overview');
    
    // Set the Overview nav link as active
    const overviewLink = document.querySelector('.nav-link[href="#overview"]');
    if (overviewLink) {
        overviewLink.classList.add('active');
    }
}

// Show specific section - Updated version
function showSection(sectionId) {
    console.log('Showing section:', sectionId);
    
    const sections = document.querySelectorAll('.section');
    
    // Hide all sections
    sections.forEach(section => {
        section.style.display = 'none';
        section.classList.remove('active');
    });
    
    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.style.display = 'block';
        targetSection.classList.add('active');
        console.log('Section shown successfully:', sectionId);
    } else {
        console.error('Section not found:', sectionId);
    }
}

// Load overview data
function loadOverviewData() {
    console.log('Loading overview data...');
    
    // Update stats
    const totalPatientsEl = document.getElementById('total-patients');
    const activeHospitalsEl = document.getElementById('active-hospitals');
    const consentRateEl = document.getElementById('consent-rate');
    const modelAccuracyEl = document.getElementById('model-accuracy');
    
    if (totalPatientsEl) totalPatientsEl.textContent = appData.global_stats.total_patients.toLocaleString();
    if (activeHospitalsEl) activeHospitalsEl.textContent = appData.global_stats.active_nodes;
    if (consentRateEl) consentRateEl.textContent = appData.global_stats.overall_consent_rate + '%';
    if (modelAccuracyEl) modelAccuracyEl.textContent = (appData.global_stats.model_accuracy * 100).toFixed(1) + '%';
    
    // Load hospital list
    const hospitalList = document.getElementById('hospital-list');
    if (hospitalList) {
        hospitalList.innerHTML = appData.hospitals.map(hospital => {
            const consentClass = hospital.consent_rate > 70 ? 'consent-high' : 
                               hospital.consent_rate > 65 ? 'consent-medium' : 'consent-low';
            return `
                <div class="hospital-item">
                    <span class="hospital-name">${hospital.name}</span>
                    <span class="hospital-consent ${consentClass}">${hospital.consent_rate.toFixed(1)}%</span>
                </div>
            `;
        }).join('');
    }
    
    // Load activity feed
    const activityFeed = document.getElementById('activity-feed');
    if (activityFeed) {
        const activities = [
            "Training round 3 completed with 85.2% accuracy",
            "New patient consent received from Metro General",
            "Smart contract updated for data privacy",
            "Blockchain validation completed for 127 transactions",
            "Model weights synchronized across all nodes"
        ];
        
        activityFeed.innerHTML = activities.map(activity => 
            `<div class="activity-item">${activity}</div>`
        ).join('');
    }
    
    console.log('Overview data loaded successfully');
}

// Load patient portal
function loadPatientPortal() {
    console.log('Loading patient portal...');
    displayPatients(appData.sample_patients);
    
    // Add search functionality
    const searchInput = document.getElementById('patient-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            searchPatient();
        });
    }
}

function displayPatients(patients) {
    let patientResults = document.getElementById('patient-results');
    if (!patientResults) return;
    
    let grid = patientResults.querySelector('.patient-grid');
    if (!grid) {
        patientResults.innerHTML = '<div class="patient-grid"></div>';
        grid = patientResults.querySelector('.patient-grid');
    }
    
    grid.innerHTML = patients.map(patient => `
        <div class="patient-card">
            <div class="patient-header">
                <div class="patient-id">${patient.id}</div>
                <div class="status ${patient.consented ? 'status--success' : 'status--error'}">
                    ${patient.consented ? 'Consented' : 'Not Consented'}
                </div>
            </div>
            <div class="patient-details">
                <div class="detail-item">
                    <div class="detail-label">Age</div>
                    <div class="detail-value">${patient.age}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Gender</div>
                    <div class="detail-value">${patient.gender}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Condition</div>
                    <div class="detail-value">${patient.condition}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Hospital</div>
                    <div class="detail-value">${patient.hospital}</div>
                </div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Wallet Address</div>
                <div class="wallet-address">${patient.wallet}</div>
            </div>
            <div class="consent-toggle">
                <div class="consent-status">
                    <div class="consent-indicator ${patient.consented ? 'active' : 'inactive'}"></div>
                    <span>Data Consent</span>
                </div>
                <button class="btn btn--sm ${patient.consented ? 'btn--outline' : 'btn--primary'}" 
                        onclick="toggleConsent('${patient.id}')">
                    ${patient.consented ? 'Revoke' : 'Grant'} Consent
                </button>
            </div>
        </div>
    `).join('');
}

function searchPatient() {
    const searchInput = document.getElementById('patient-search');
    if (!searchInput) return;
    
    const searchTerm = searchInput.value.toLowerCase();
    if (!searchTerm) {
        displayPatients(appData.sample_patients);
        return;
    }
    
    const filteredPatients = appData.sample_patients.filter(patient => 
        patient.id.toLowerCase().includes(searchTerm) ||
        patient.condition.toLowerCase().includes(searchTerm) ||
        patient.hospital.toLowerCase().includes(searchTerm) ||
        patient.gender.toLowerCase().includes(searchTerm)
    );
    
    displayPatients(filteredPatients);
}

function toggleConsent(patientId) {
    const patient = appData.sample_patients.find(p => p.id === patientId);
    if (patient) {
        patient.consented = !patient.consented;
        if (patient.consented) {
            patient.consent_date = new Date().toISOString().split('T')[0];
            patient.expiry = new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
        } else {
            patient.consent_date = null;
            patient.expiry = null;
        }
        displayPatients(appData.sample_patients);
        
        // Simulate blockchain transaction
        const transaction = {
            hash: `0x${Math.random().toString(16).substring(2, 15)}`,
            type: patient.consented ? "CONSENT_GRANT" : "CONSENT_REVOKE",
            patient: patientId,
            timestamp: new Date().toLocaleString(),
            status: "confirmed"
        };
        appData.blockchain_transactions.unshift(transaction);
        loadBlockchainData();
    }
}

// Load hospital dashboard - Fixed version
function loadHospitalDashboard() {
    console.log('Loading hospital dashboard...');
    
    const hospitalSelect = document.getElementById('hospital-select');
    if (hospitalSelect) {
        // Clear existing options
        hospitalSelect.innerHTML = '';
        
        // Add default option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Select a hospital...';
        hospitalSelect.appendChild(defaultOption);
        
        // Add hospital options
        appData.hospitals.forEach(hospital => {
            const option = document.createElement('option');
            option.value = hospital.id;
            option.textContent = hospital.name;
            hospitalSelect.appendChild(option);
        });
        
        // Add change event listener
        hospitalSelect.addEventListener('change', function() {
            console.log('Hospital selected:', this.value);
            if (this.value) {
                displayHospitalStats(this.value);
            } else {
                const statsContainer = document.getElementById('hospital-stats');
                if (statsContainer) {
                    statsContainer.innerHTML = '';
                }
            }
        });
        
        console.log('Hospital dashboard loaded successfully');
    } else {
        console.error('Hospital select element not found');
    }
}

function displayHospitalStats(hospitalId) {
    const hospital = appData.hospitals.find(h => h.id === hospitalId);
    if (!hospital) return;
    
    const statsContainer = document.getElementById('hospital-stats');
    if (statsContainer) {
        statsContainer.innerHTML = `
            <div class="stat-card">
                <div class="stat-number">${hospital.patients.toLocaleString()}</div>
                <div class="stat-label">Total Patients</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${hospital.consented.toLocaleString()}</div>
                <div class="stat-label">Consented Patients</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${hospital.consent_rate.toFixed(1)}%</div>
                <div class="stat-label">Consent Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${(hospital.patients - hospital.consented).toLocaleString()}</div>
                <div class="stat-label">Pending Consent</div>
            </div>
        `;
        console.log('Hospital stats displayed for:', hospital.name);
    }
}

// Training functionality
function startTraining() {
    console.log('Starting training...');
    
    const startBtn = document.getElementById('start-training');
    const stopBtn = document.getElementById('stop-training');
    
    if (startBtn) startBtn.disabled = true;
    if (stopBtn) stopBtn.disabled = false;
    
    currentTrainingRound = 0;
    const epochsSelect = document.getElementById('epochs');
    const maxRounds = epochsSelect ? parseInt(epochsSelect.value) : 10;
    
    // Clear previous training data
    if (charts.training) {
        charts.training.data.labels = [];
        charts.training.data.datasets[0].data = [];
        charts.training.data.datasets[1].data = [];
        charts.training.update();
    }
    
    trainingInterval = setInterval(() => {
        currentTrainingRound++;
        
        // Simulate training metrics
        const accuracy = 0.7 + (Math.random() * 0.15) + (currentTrainingRound * 0.015);
        const loss = Math.max(0.1, 0.5 - (currentTrainingRound * 0.04) + (Math.random() * 0.08));
        
        updateTrainingStatus(currentTrainingRound, accuracy, loss);
        updateTrainingChart(currentTrainingRound, accuracy, loss);
        
        if (currentTrainingRound >= maxRounds) {
            stopTraining();
        }
    }, 1500);
    
    console.log('Training started with max rounds:', maxRounds);
}

function stopTraining() {
    console.log('Stopping training...');
    
    if (trainingInterval) {
        clearInterval(trainingInterval);
        trainingInterval = null;
    }
    
    const startBtn = document.getElementById('start-training');
    const stopBtn = document.getElementById('stop-training');
    
    if (startBtn) startBtn.disabled = false;
    if (stopBtn) stopBtn.disabled = true;
}

function updateTrainingStatus(round, accuracy, loss) {
    const currentRoundEl = document.getElementById('current-round');
    const accuracyEl = document.getElementById('training-accuracy');
    const lossEl = document.getElementById('training-loss');
    
    if (currentRoundEl) currentRoundEl.textContent = round;
    if (accuracyEl) accuracyEl.textContent = (accuracy * 100).toFixed(1) + '%';
    if (lossEl) lossEl.textContent = loss.toFixed(3);
}

function updateTrainingChart(round, accuracy, loss) {
    if (charts.training) {
        charts.training.data.labels.push(`Round ${round}`);
        charts.training.data.datasets[0].data.push((accuracy * 100).toFixed(1));
        charts.training.data.datasets[1].data.push(loss.toFixed(3));
        charts.training.update('none');
    }
}

// Load blockchain data
function loadBlockchainData() {
    console.log('Loading blockchain data...');
    
    const transactionList = document.getElementById('transaction-list');
    if (transactionList) {
        transactionList.innerHTML = appData.blockchain_transactions.slice(0, 10).map(tx => `
            <div class="transaction-item">
                <div>
                    <div class="transaction-hash">${tx.hash}</div>
                    <div class="transaction-type">${tx.type.replace(/_/g, ' ')}</div>
                </div>
                <div>
                    <div style="font-size: var(--font-size-sm); color: var(--color-text-secondary);">${tx.timestamp}</div>
                    <div class="status status--success">${tx.status}</div>
                </div>
            </div>
        `).join('');
        
        console.log('Blockchain data loaded successfully');
    }
}

// Initialize all charts
function initializeCharts() {
    console.log('Initializing charts...');
    try {
        initializeAgeConsentChart();
        initializeConditionsChart();
        initializeTrainingChart();
        initializeNodesChart();
        initializeConsentTrendsChart();
        initializeHospitalComparisonChart();
        initializeAgeAnalysisChart();
        initializeConditionsStatsChart();
        console.log('Charts initialized successfully');
    } catch (error) {
        console.error('Error initializing charts:', error);
    }
}

// Chart initialization functions (same as before but with better error handling)
function initializeAgeConsentChart() {
    const ctx = document.getElementById('age-consent-chart');
    if (!ctx || charts.ageConsent) return;
    
    try {
        charts.ageConsent = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['18-30', '31-45', '46-60', '61-75', '76+'],
                datasets: [{
                    label: 'Consent Rate (%)',
                    data: [62, 71, 74, 66, 58],
                    backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating age consent chart:', error);
    }
}

function initializeConditionsChart() {
    const ctx = document.getElementById('conditions-chart');
    if (!ctx || charts.conditions) return;
    
    try {
        charts.conditions = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Hypertension', 'Diabetes', 'Heart Disease', 'Cancer', 'Other'],
                datasets: [{
                    data: [35, 25, 20, 10, 10],
                    backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    } catch (error) {
        console.error('Error creating conditions chart:', error);
    }
}

function initializeTrainingChart() {
    const ctx = document.getElementById('training-chart');
    if (!ctx || charts.training) return;
    
    try {
        charts.training = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Accuracy (%)',
                    data: [],
                    borderColor: '#1FB8CD',
                    backgroundColor: 'rgba(31, 184, 205, 0.1)',
                    yAxisID: 'y'
                }, {
                    label: 'Loss',
                    data: [],
                    borderColor: '#B4413C',
                    backgroundColor: 'rgba(180, 65, 60, 0.1)',
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Accuracy (%)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Loss'
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating training chart:', error);
    }
}

function initializeNodesChart() {
    const ctx = document.getElementById('nodes-chart');
    if (!ctx || charts.nodes) return;
    
    try {
        charts.nodes = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: appData.hospitals.map(h => h.name.split(' ')[0]),
                datasets: [{
                    label: 'Total Patients',
                    data: appData.hospitals.map(h => h.patients),
                    backgroundColor: '#1FB8CD'
                }, {
                    label: 'Consented Patients',
                    data: appData.hospitals.map(h => h.consented),
                    backgroundColor: '#FFC185'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    } catch (error) {
        console.error('Error creating nodes chart:', error);
    }
}

function initializeConsentTrendsChart() {
    const ctx = document.getElementById('consent-trends-chart');
    if (!ctx || charts.consentTrends) return;
    
    try {
        charts.consentTrends = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Consent Rate (%)',
                    data: [62, 65, 67, 66, 68, 69],
                    borderColor: '#1FB8CD',
                    backgroundColor: 'rgba(31, 184, 205, 0.1)',
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    } catch (error) {
        console.error('Error creating consent trends chart:', error);
    }
}

function initializeHospitalComparisonChart() {
    const ctx = document.getElementById('hospital-comparison-chart');
    if (!ctx || charts.hospitalComparison) return;
    
    try {
        charts.hospitalComparison = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: appData.hospitals.map(h => h.name.split(' ')[0]),
                datasets: [{
                    label: 'Consent Rate (%)',
                    data: appData.hospitals.map(h => h.consent_rate),
                    backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F', '#DB4545', '#D2BA4C', '#964325']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating hospital comparison chart:', error);
    }
}

function initializeAgeAnalysisChart() {
    const ctx = document.getElementById('age-analysis-chart');
    if (!ctx || charts.ageAnalysis) return;
    
    try {
        charts.ageAnalysis = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['18-30', '31-45', '46-60', '61-75', '76+'],
                datasets: [{
                    data: [18, 28, 25, 20, 9],
                    backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    } catch (error) {
        console.error('Error creating age analysis chart:', error);
    }
}

function initializeConditionsStatsChart() {
    const ctx = document.getElementById('conditions-stats-chart');
    if (!ctx || charts.conditionsStats) return;
    
    try {
        charts.conditionsStats = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Prevalence', 'Consent Rate', 'Data Quality', 'Treatment Success', 'Research Value'],
                datasets: [{
                    label: 'Hypertension',
                    data: [85, 72, 88, 75, 82],
                    borderColor: '#1FB8CD',
                    backgroundColor: 'rgba(31, 184, 205, 0.2)'
                }, {
                    label: 'Diabetes',
                    data: [70, 68, 85, 82, 90],
                    borderColor: '#FFC185',
                    backgroundColor: 'rgba(255, 193, 133, 0.2)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating conditions stats chart:', error);
    }
}