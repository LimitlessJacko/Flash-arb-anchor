// Flash Arbitrage Bot Dashboard JavaScript

class FlashArbitrageDashboard {
    constructor() {
        this.isRunning = false;
        this.updateInterval = null;
        this.chart = null;
        this.profitHistory = [];
        this.currentStep = 0;
        this.maxSteps = 3;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.initChart();
        this.updateStatus();
        this.loadConfiguration();
        
        // Start auto-refresh
        this.startAutoRefresh();
    }
    
    setupEventListeners() {
        // Bot control buttons
        document.getElementById('startBtn').addEventListener('click', () => this.startBot());
        document.getElementById('stopBtn').addEventListener('click', () => this.stopBot());
        
        // Configuration
        document.getElementById('saveConfigBtn').addEventListener('click', () => this.saveConfiguration());
        
        // Opportunities refresh
        document.getElementById('refreshOpportunities').addEventListener('click', () => this.refreshOpportunities());
        
        // Setup modal
        this.setupModalEventListeners();
        
        // Show setup modal on first load
        if (!localStorage.getItem('flash_arb_setup_complete')) {
            this.showSetupModal();
        }
    }
    
    setupModalEventListeners() {
        const modal = document.getElementById('setupModal');
        const closeBtn = modal.querySelector('.close');
        const prevBtn = document.getElementById('prevStep');
        const nextBtn = document.getElementById('nextStep');
        const completeBtn = document.getElementById('completeSetup');
        
        closeBtn.addEventListener('click', () => this.hideSetupModal());
        prevBtn.addEventListener('click', () => this.previousStep());
        nextBtn.addEventListener('click', () => this.nextStep());
        completeBtn.addEventListener('click', () => this.completeSetup());
        
        // Close modal when clicking outside
        window.addEventListener('click', (event) => {
            if (event.target === modal) {
                this.hideSetupModal();
            }
        });
    }
    
    showSetupModal() {
        document.getElementById('setupModal').style.display = 'block';
        this.currentStep = 0;
        this.updateSetupStep();
    }
    
    hideSetupModal() {
        document.getElementById('setupModal').style.display = 'none';
    }
    
    updateSetupStep() {
        const steps = document.querySelectorAll('.setup-step');
        const prevBtn = document.getElementById('prevStep');
        const nextBtn = document.getElementById('nextStep');
        const completeBtn = document.getElementById('completeSetup');
        
        // Hide all steps
        steps.forEach(step => step.classList.remove('active'));
        
        // Show current step
        if (steps[this.currentStep]) {
            steps[this.currentStep].classList.add('active');
        }
        
        // Update button visibility
        prevBtn.style.display = this.currentStep > 0 ? 'block' : 'none';
        nextBtn.style.display = this.currentStep < this.maxSteps - 1 ? 'block' : 'none';
        completeBtn.style.display = this.currentStep === this.maxSteps - 1 ? 'block' : 'none';
    }
    
    previousStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.updateSetupStep();
        }
    }
    
    nextStep() {
        if (this.currentStep < this.maxSteps - 1) {
            this.currentStep++;
            this.updateSetupStep();
        }
    }
    
    completeSetup() {
        // Collect all setup data
        const setupData = {
            walletAddress: document.getElementById('walletAddress').value,
            privateKey: document.getElementById('privateKey').value,
            raydiumApi: document.getElementById('raydiumApi').value,
            orcaApi: document.getElementById('orcaApi').value,
            minProfit: parseFloat(document.getElementById('setupMinProfit').value),
            maxRisk: parseFloat(document.getElementById('setupMaxRisk').value)
        };
        
        // Save setup data
        localStorage.setItem('flash_arb_setup_data', JSON.stringify(setupData));
        localStorage.setItem('flash_arb_setup_complete', 'true');
        
        // Apply configuration
        this.applySetupConfiguration(setupData);
        
        this.hideSetupModal();
        this.showNotification('Setup completed successfully!', 'success');
    }
    
    applySetupConfiguration(setupData) {
        // Update configuration inputs
        document.getElementById('minProfit').value = setupData.minProfit;
        
        // Save configuration
        this.saveConfiguration();
    }
    
    async startBot() {
        try {
            const config = this.getConfiguration();
            
            const response = await fetch('/api/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(config)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.isRunning = true;
                this.updateButtonStates();
                this.showNotification('Bot started successfully!', 'success');
            } else {
                this.showNotification(result.error || 'Failed to start bot', 'error');
            }
        } catch (error) {
            this.showNotification('Error starting bot: ' + error.message, 'error');
        }
    }
    
    async stopBot() {
        try {
            const response = await fetch('/api/stop', {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.isRunning = false;
                this.updateButtonStates();
                this.showNotification('Bot stopped successfully!', 'success');
            } else {
                this.showNotification(result.error || 'Failed to stop bot', 'error');
            }
        } catch (error) {
            this.showNotification('Error stopping bot: ' + error.message, 'error');
        }
    }
    
    updateButtonStates() {
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        
        if (this.isRunning) {
            startBtn.style.display = 'none';
            stopBtn.style.display = 'inline-flex';
            statusIndicator.classList.add('running');
            statusText.textContent = 'Running';
        } else {
            startBtn.style.display = 'inline-flex';
            stopBtn.style.display = 'none';
            statusIndicator.classList.remove('running');
            statusText.textContent = 'Stopped';
        }
    }
    
    getConfiguration() {
        return {
            min_profit_threshold: parseFloat(document.getElementById('minProfit').value) / 100,
            max_gas_cost: parseFloat(document.getElementById('maxGas').value),
            max_slippage: parseFloat(document.getElementById('maxSlippage').value) / 100,
            max_position_size: parseFloat(document.getElementById('maxPosition').value)
        };
    }
    
    async saveConfiguration() {
        try {
            const config = this.getConfiguration();
            
            const response = await fetch('/api/config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(config)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.showNotification('Configuration saved successfully!', 'success');
            } else {
                this.showNotification(result.error || 'Failed to save configuration', 'error');
            }
        } catch (error) {
            this.showNotification('Error saving configuration: ' + error.message, 'error');
        }
    }
    
    async loadConfiguration() {
        try {
            const response = await fetch('/api/config');
            const config = await response.json();
            
            if (response.ok && Object.keys(config).length > 0) {
                document.getElementById('minProfit').value = (config.min_profit_threshold * 100).toFixed(3);
                document.getElementById('maxGas').value = config.max_gas_cost.toFixed(3);
                document.getElementById('maxSlippage').value = (config.max_slippage * 100).toFixed(1);
                document.getElementById('maxPosition').value = config.max_position_size;
            }
        } catch (error) {
            console.error('Error loading configuration:', error);
        }
    }
    
    async updateStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (response.ok) {
                this.isRunning = data.status === 'running';
                this.updateButtonStates();
                
                if (data.statistics) {
                    this.updateStatistics(data.statistics);
                }
            }
        } catch (error) {
            console.error('Error updating status:', error);
        }
    }
    
    updateStatistics(stats) {
        document.getElementById('totalProfit').textContent = `${stats.total_profit?.toFixed(4) || '0.0000'} SOL`;
        document.getElementById('successRate').textContent = `${(stats.success_rate * 100)?.toFixed(1) || '0'}%`;
        document.getElementById('totalTrades').textContent = (stats.successful_trades + stats.failed_trades) || '0';
        document.getElementById('opportunitiesCount').textContent = stats.opportunities_count || '0';
        
        // Update engine comparison
        document.getElementById('pythonProfit').textContent = `${stats.total_profit?.toFixed(4) || '0.0000'} SOL`;
        document.getElementById('pythonTrades').textContent = (stats.successful_trades + stats.failed_trades) || '0';
        document.getElementById('pythonSuccessRate').textContent = `${(stats.success_rate * 100)?.toFixed(1) || '0'}%`;
        
        // Update chart
        this.updateChart(stats.total_profit || 0);
    }
    
    async refreshOpportunities() {
        try {
            const response = await fetch('/api/opportunities');
            const data = await response.json();
            
            if (response.ok) {
                this.updateOpportunitiesTable(data.opportunities);
            }
            
            // Also get C++ engine opportunities
            const cppResponse = await fetch('/api/cpp/opportunities');
            if (cppResponse.ok) {
                const cppData = await cppResponse.json();
                // Merge with Python opportunities if needed
            }
        } catch (error) {
            console.error('Error refreshing opportunities:', error);
        }
    }
    
    updateOpportunitiesTable(opportunities) {
        const tbody = document.getElementById('opportunitiesTable');
        
        if (!opportunities || opportunities.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="no-data">No opportunities found</td></tr>';
            return;
        }
        
        tbody.innerHTML = opportunities.map((opp, index) => `
            <tr>
                <td>${opp.token_pair}</td>
                <td>${opp.exchange_a}</td>
                <td>${opp.exchange_b}</td>
                <td>${opp.price_diff?.toFixed(6) || 'N/A'}</td>
                <td>${(opp.profit_potential * 100)?.toFixed(2) || 'N/A'}%</td>
                <td>${opp.net_profit?.toFixed(4) || 'N/A'} SOL</td>
                <td>${(opp.confidence * 100)?.toFixed(0) || 'N/A'}%</td>
                <td>
                    <button class="btn btn-primary btn-sm" onclick="dashboard.executeOpportunity(${index})">
                        Execute
                    </button>
                </td>
            </tr>
        `).join('');
    }
    
    async executeOpportunity(index) {
        try {
            const response = await fetch(`/api/cpp/execute/${index}`, {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (response.ok) {
                if (result.success) {
                    this.showNotification('Trade executed successfully!', 'success');
                } else {
                    this.showNotification('Trade execution failed', 'warning');
                }
                
                // Refresh data
                this.updateStatus();
                this.refreshOpportunities();
            } else {
                this.showNotification(result.error || 'Failed to execute trade', 'error');
            }
        } catch (error) {
            this.showNotification('Error executing trade: ' + error.message, 'error');
        }
    }
    
    initChart() {
        const ctx = document.getElementById('performanceChart').getContext('2d');
        
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Cumulative Profit (SOL)',
                    data: [],
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Profit (SOL)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    }
    
    updateChart(profit) {
        const now = new Date().toLocaleTimeString();
        
        this.profitHistory.push({ time: now, profit: profit });
        
        // Keep only last 50 data points
        if (this.profitHistory.length > 50) {
            this.profitHistory.shift();
        }
        
        this.chart.data.labels = this.profitHistory.map(p => p.time);
        this.chart.data.datasets[0].data = this.profitHistory.map(p => p.profit);
        this.chart.update();
    }
    
    startAutoRefresh() {
        this.updateInterval = setInterval(() => {
            this.updateStatus();
            this.refreshOpportunities();
            this.updateCppEngineStats();
        }, 5000); // Update every 5 seconds
    }
    
    async updateCppEngineStats() {
        try {
            const response = await fetch('/api/cpp/status');
            if (response.ok) {
                const stats = await response.json();
                
                document.getElementById('cppProfit').textContent = `${stats.total_profit?.toFixed(4) || '0.0000'} SOL`;
                document.getElementById('cppTrades').textContent = (stats.successful_trades + stats.failed_trades) || '0';
                document.getElementById('cppSuccessRate').textContent = `${(stats.success_rate * 100)?.toFixed(1) || '0'}%`;
            }
        } catch (error) {
            console.error('Error updating C++ engine stats:', error);
        }
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()">&times;</button>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 15px;
            min-width: 300px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        `;
        
        // Set background color based on type
        const colors = {
            success: '#28a745',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#17a2b8'
        };
        notification.style.backgroundColor = colors[type] || colors.info;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }
}

// Download source code function
function downloadSourceCode() {
    const sourceFiles = [
        'arbitrage_engine.py',
        'app.py',
        'arbitrage_wrapper.py',
        'templates/index.html',
        'static/css/style.css',
        'static/js/dashboard.js'
    ];
    
    // Create a simple download link for the main files
    const link = document.createElement('a');
    link.href = '/download/arbitrage_engine.py';
    link.download = 'arbitrage_engine.py';
    link.click();
}

// Initialize dashboard when page loads
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new FlashArbitrageDashboard();
});

