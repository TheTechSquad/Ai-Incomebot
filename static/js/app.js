/**
 * AI INCOME Web App JavaScript
 * Enhanced functionality for Telegram Web App integration
 */

// Telegram Web App instance (with fallback)
const tg = window.Telegram?.WebApp || null;

// App initialization
document.addEventListener('DOMContentLoaded', function() {
    console.log('App initializing...', tg ? 'Telegram mode' : 'Browser mode');
    initializeApp();
    setupEventListeners();
    configureTheme();
});

/**
 * Initialize the application
 */
function initializeApp() {
    if (tg) {
        // Configure Telegram Web App
        tg.ready();
        tg.expand();
        
        // Enable closing confirmation
        tg.enableClosingConfirmation();
        
        // Set up main button if needed
        setupMainButton();
        
        // Handle back button
        if (tg.BackButton) {
            tg.BackButton.onClick(() => {
                if (isModalOpen()) {
                    closeAllModals();
                } else {
                    tg.close();
                }
            });
        }
    }
    
    // Initialize page-specific features
    const currentPage = getCurrentPage();
    switch (currentPage) {
        case 'dashboard':
            initializeDashboard();
            break;
        case 'shop':
            initializeShop();
            break;
        default:
            initializeLanding();
    }
}

/**
 * Setup global event listeners
 */
function setupEventListeners() {
    // Handle modal close on background click
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target.id);
        }
    });
    
    // Handle escape key for modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && isModalOpen()) {
            closeAllModals();
        }
    });
    
    // Handle online/offline status
    window.addEventListener('online', handleOnlineStatus);
    window.addEventListener('offline', handleOfflineStatus);
    
    // Handle visibility change (when user switches tabs)
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    // Add haptic feedback to interactive elements
    addHapticFeedback();
}

/**
 * Configure theme based on Telegram Web App theme
 */
function configureTheme() {
    if (!tg) return;
    
    const themeParams = tg.themeParams;
    const root = document.documentElement;
    
    // Apply Telegram theme colors
    if (themeParams.bg_color) {
        root.style.setProperty('--tg-theme-bg-color', themeParams.bg_color);
    }
    
    if (themeParams.text_color) {
        root.style.setProperty('--tg-theme-text-color', themeParams.text_color);
    }
    
    if (themeParams.button_color) {
        root.style.setProperty('--tg-theme-button-color', themeParams.button_color);
    }
    
    if (themeParams.secondary_bg_color) {
        root.style.setProperty('--tg-theme-secondary-color', themeParams.secondary_bg_color);
    }
    
    // Handle dark theme
    if (tg.colorScheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
}

/**
 * Setup Telegram Web App main button
 */
function setupMainButton() {
    if (!tg?.MainButton) return;
    
    const currentPage = getCurrentPage();
    
    switch (currentPage) {
        case 'dashboard':
            tg.MainButton.text = '⛏️ START MINING';
            tg.MainButton.onClick(startMining);
            tg.MainButton.show();
            break;
        case 'shop':
            tg.MainButton.hide();
            break;
        default:
            tg.MainButton.text = '🚀 OPEN BOT';
            tg.MainButton.onClick(() => {
                tg.openTelegramLink('https://t.me/AI_IncomeBot');
            });
            tg.MainButton.show();
    }
}

/**
 * Get current page identifier
 */
function getCurrentPage() {
    const path = window.location.pathname;
    if (path.includes('dashboard')) return 'dashboard';
    if (path.includes('shop')) return 'shop';
    return 'landing';
}

/**
 * Dashboard page initialization
 */
function initializeDashboard() {
    // Auto-refresh stats periodically
    startStatsRefresh();
    
    // Initialize mining progress tracking
    initializeMiningTracking();
    
    // Setup achievement animations
    animateAchievements();
    
    // Initialize daily bonus timer
    startDailyBonusTimer();
}

/**
 * Shop page initialization
 */
function initializeShop() {
    // Initialize package animations
    animatePackageCards();
    
    // Setup calculator
    initializeCalculator();
    
    // Add purchase tracking
    trackPurchaseInteractions();
}

/**
 * Landing page initialization
 */
function initializeLanding() {
    // Initialize testimonials carousel
    initializeTestimonialsCarousel();
    
    // Setup FAQ interactions
    initializeFAQ();
    
    // Add scroll animations
    initializeScrollAnimations();
}

/**
 * Enhanced Mining Function with Progress Tracking
 */
async function startMining() {
    if (!validateMining()) return;
    
    showModal('mining-modal');
    
    // Disable mining during process
    setMiningState(false);
    
    try {
        // Animate mining progress
        await animateMiningProgress();
        
        // Call mining API
        const result = await apiRequest('/api/mine');
        
        closeModal('mining-modal');
        
        if (result.success) {
            // Show success with enhanced animation
            showMiningSuccess(result);
            
            // Update UI
            updateMiningStats(result);
            
            // Haptic feedback for success
            triggerHaptic('success');
            
            // Update Telegram Web App data
            updateTelegramData(result);
            
        } else {
            throw new Error(result.error || 'Mining failed');
        }
        
    } catch (error) {
        closeModal('mining-modal');
        showError(error.message);
        triggerHaptic('error');
    } finally {
        setMiningState(true);
    }
}

/**
 * Validate mining conditions
 */
function validateMining() {
    // Check if user is online
    if (!navigator.onLine) {
        showError('Please check your internet connection');
        return false;
    }
    
    // Check if already mining
    if (isMining()) {
        showError('Mining in progress, please wait');
        return false;
    }
    
    return true;
}

/**
 * Animate mining progress with realistic steps
 */
async function animateMiningProgress() {
    return new Promise((resolve) => {
        let progress = 0;
        const progressBar = document.getElementById('mining-progress');
        const statusText = document.getElementById('mining-status');
        
        const stages = [
            { progress: 15, text: 'Connecting to mining pool...', delay: 500 },
            { progress: 30, text: 'Initializing GPU cores...', delay: 800 },
            { progress: 45, text: 'Loading blockchain data...', delay: 600 },
            { progress: 60, text: 'Processing hash algorithms...', delay: 900 },
            { progress: 75, text: 'Validating proof of work...', delay: 700 },
            { progress: 90, text: 'Calculating rewards...', delay: 500 },
            { progress: 100, text: 'Finalizing results...', delay: 400 }
        ];
        
        let currentStage = 0;
        
        const progressInterval = setInterval(() => {
            if (currentStage < stages.length) {
                const stage = stages[currentStage];
                progress = stage.progress;
                
                // Smooth progress animation
                progressBar.style.width = progress + '%';
                statusText.textContent = stage.text;
                
                // Add some randomness for realism
                if (Math.random() > 0.7) {
                    progress += Math.random() * 3;
                }
                
                setTimeout(() => {
                    currentStage++;
                    if (currentStage >= stages.length) {
                        clearInterval(progressInterval);
                        resolve();
                    }
                }, stage.delay);
                
            }
        }, 100);
    });
}

/**
 * Show enhanced mining success animation
 */
function showMiningSuccess(result) {
    const modal = document.getElementById('success-modal');
    const title = document.getElementById('success-title');
    const message = document.getElementById('success-message');
    
    title.innerHTML = '🎉 Mining Successful!';
    message.innerHTML = `
        <div class="success-details">
            <div class="earning-highlight">
                <span class="hash-earned">+${result.hashes_earned.toFixed(6)}</span>
                <span class="hash-label">Hashes Mined</span>
            </div>
            <div class="usdt-earned">
                Worth $${(result.hashes_earned * 0.01).toFixed(4)} USDT
            </div>
            <div class="total-stats">
                Total: ${result.total_hashes.toFixed(6)} hashes ($${result.usdt_value.toFixed(2)})
            </div>
        </div>
    `;
    
    showModal('success-modal');
    
    // Add confetti animation
    createConfettiEffect();
}

/**
 * Update mining statistics in UI
 */
function updateMiningStats(result) {
    // Update stat cards
    const hashElement = document.querySelector('.stat-card.success .stat-value');
    const usdtElement = document.querySelector('.stat-card.warning .stat-value');
    
    if (hashElement) {
        animateCounter(hashElement, parseFloat(hashElement.textContent), result.total_hashes, 6);
    }
    
    if (usdtElement) {
        const currentValue = parseFloat(usdtElement.textContent.replace('$', ''));
        animateCounter(usdtElement, currentValue, result.usdt_value, 2, '$');
    }
    
    // Update balance in header if present
    const balanceElement = document.querySelector('.user-balance span');
    if (balanceElement) {
        balanceElement.textContent = `$${result.usdt_value.toFixed(2)}`;
    }
}

/**
 * Enhanced Stats Loading with Caching
 */
async function showStats() {
    try {
        showModal('stats-modal');
        
        // Show loading state
        document.getElementById('stats-content').innerHTML = `
            <div class="stats-loading">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Loading statistics...</p>
            </div>
        `;
        
        // Try to get cached stats first
        const cachedStats = getCachedStats();
        if (cachedStats && isCacheValid()) {
            displayStats(cachedStats);
        }
        
        // Fetch fresh stats
        const result = await apiRequest('/api/stats');
        
        if (result.error) {
            throw new Error(result.error);
        }
        
        // Cache and display stats
        cacheStats(result);
        displayStats(result);
        
    } catch (error) {
        document.getElementById('stats-content').innerHTML = `
            <div class="stats-error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load statistics</p>
                <button onclick="showStats()" class="btn btn-primary btn-sm">Retry</button>
            </div>
        `;
    }
}

/**
 * Display stats with enhanced formatting
 */
function displayStats(result) {
    document.getElementById('stats-content').innerHTML = `
        <div class="stats-grid">
            <div class="stat-item">
                <i class="fas fa-bolt" style="color: #FF9800;"></i>
                <span class="stat-label">GPU Power</span>
                <span class="stat-value">${result.gpu_power.toLocaleString()}</span>
            </div>
            <div class="stat-item">
                <i class="fas fa-coins" style="color: #4CAF50;"></i>
                <span class="stat-label">Total Hashes</span>
                <span class="stat-value">${result.total_hashes.toFixed(6)}</span>
            </div>
            <div class="stat-item">
                <i class="fas fa-dollar-sign" style="color: #2196F3;"></i>
                <span class="stat-label">USDT Value</span>
                <span class="stat-value">$${result.usdt_value.toFixed(2)}</span>
            </div>
            <div class="stat-item">
                <i class="fas fa-chart-line" style="color: #9C27B0;"></i>
                <span class="stat-label">Daily Estimate</span>
                <span class="stat-value">$${result.daily_estimate.toFixed(2)}</span>
            </div>
            <div class="stat-item">
                <i class="fas fa-link" style="color: #FF5722;"></i>
                <span class="stat-label">Referral Code</span>
                <span class="stat-value">${result.referral_code}</span>
            </div>
            <div class="stat-item">
                <i class="fas fa-user-clock" style="color: #607D8B;"></i>
                <span class="stat-label">Member Since</span>
                <span class="stat-value">${result.member_since}</span>
            </div>
        </div>
        <div class="stats-actions">
            <button class="btn btn-primary" onclick="shareStats()">
                <i class="fas fa-share"></i> Share Progress
            </button>
            <button class="btn btn-secondary" onclick="exportStats()">
                <i class="fas fa-download"></i> Export Data
            </button>
        </div>
    `;
}

/**
 * Enhanced Purchase Flow with Validation
 */
async function purchasePackage(packageId) {
    const packages = getPackageData();
    const selectedPackage = packages.find(p => p.id === packageId);
    
    if (!selectedPackage) {
        showError('Package not found');
        return;
    }
    
    // Show confirmation modal
    showPurchaseConfirmation(selectedPackage);
}

/**
 * Show purchase confirmation with enhanced UI
 */
function showPurchaseConfirmation(package) {
    document.getElementById('package-summary').innerHTML = `
        <div class="purchase-header">
            <div class="package-icon">
                <i class="fas fa-gem"></i>
            </div>
            <h4>$${package.price} GPU Power Package</h4>
        </div>
        <div class="purchase-breakdown">
            <div class="breakdown-item">
                <span>Base GPU Power:</span>
                <span>${package.base_power.toLocaleString()}</span>
            </div>
            <div class="breakdown-item bonus">
                <span>Bonus Power (25%):</span>
                <span>+${package.bonus_power.toLocaleString()}</span>
            </div>
            <div class="breakdown-total">
                <span><strong>Total GPU Power:</strong></span>
                <span><strong>${package.total_power.toLocaleString()}</strong></span>
            </div>
            <div class="earnings-projection">
                <div class="projection-item">
                    <span>Per Mining Session:</span>
                    <span>$${((package.total_power * 0.0005) * 0.01).toFixed(4)}</span>
                </div>
                <div class="projection-item">
                    <span>Daily Potential:</span>
                    <span>$${((package.total_power * 0.0005 * 24) * 0.01).toFixed(2)}</span>
                </div>
                <div class="projection-item highlight">
                    <span>Break-even Time:</span>
                    <span>~${Math.ceil(package.price / ((package.total_power * 0.0005 * 24) * 0.01))} days</span>
                </div>
            </div>
        </div>
        <div class="purchase-warning">
            <i class="fas fa-info-circle"></i>
            <p>This is a demo purchase. In production, this would process real payment.</p>
        </div>
    `;
    
    // Store selected package for confirmation
    window.selectedPurchasePackage = package;
    
    showModal('purchase-modal');
}

/**
 * Confirm purchase with enhanced feedback
 */
async function confirmPurchase() {
    const package = window.selectedPurchasePackage;
    if (!package) return;
    
    const confirmBtn = document.getElementById('confirm-purchase-btn');
    
    // Show loading state
    setButtonLoading(confirmBtn, true);
    
    try {
        const result = await apiRequest('/api/purchase', {
            package_id: package.id
        });
        
        closeModal('purchase-modal');
        
        if (result.success) {
            showPurchaseSuccess(result, package);
            updatePowerDisplay(result.new_gpu_power);
            triggerHaptic('success');
            
            // Auto-refresh page after success
            setTimeout(() => {
                location.reload();
            }, 3000);
            
        } else {
            throw new Error(result.error || 'Purchase failed');
        }
        
    } catch (error) {
        showError(error.message);
        triggerHaptic('error');
    } finally {
        setButtonLoading(confirmBtn, false);
    }
}

/**
 * Show purchase success with celebration
 */
function showPurchaseSuccess(result, package) {
    showSuccess(
        '🎉 Purchase Successful!',
        `
        <div class="purchase-success">
            <div class="success-icon">
                <i class="fas fa-check-circle"></i>
            </div>
            <p>You've successfully purchased the <strong>$${package.price} GPU Power Package</strong>!</p>
            <div class="power-upgrade">
                <div class="power-added">
                    <span>Power Added:</span>
                    <span class="highlight">+${result.power_added.toLocaleString()}</span>
                </div>
                <div class="new-total">
                    <span>New Total:</span>
                    <span class="highlight">${result.new_gpu_power.toLocaleString()}</span>
                </div>
            </div>
            <p class="success-note">Your mining power has been increased! Start mining to see the difference.</p>
        </div>
        `
    );
    
    // Add celebration effect
    createPowerUpEffect();
}

/**
 * Utility Functions
 */

// Counter animation for numbers
function animateCounter(element, start, end, decimals = 0, prefix = '') {
    const duration = 1000;
    const increment = (end - start) / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        
        element.textContent = prefix + current.toFixed(decimals);
    }, 16);
}

// Haptic feedback integration
function triggerHaptic(type = 'light') {
    if (!tg?.HapticFeedback) return;
    
    switch (type) {
        case 'success':
            tg.HapticFeedback.notificationOccurred('success');
            break;
        case 'error':
            tg.HapticFeedback.notificationOccurred('error');
            break;
        case 'warning':
            tg.HapticFeedback.notificationOccurred('warning');
            break;
        default:
            tg.HapticFeedback.impactOccurred(type);
    }
}

// Add haptic feedback to buttons
function addHapticFeedback() {
    document.addEventListener('click', (e) => {
        const clickableElements = ['button', '.btn', '.nav-item', '.action-item', '.package-card'];
        
        for (const selector of clickableElements) {
            if (e.target.matches(selector) || e.target.closest(selector)) {
                triggerHaptic('light');
                break;
            }
        }
    });
}

// Button loading state management
function setButtonLoading(button, loading) {
    if (loading) {
        button.disabled = true;
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText || button.innerHTML;
    }
}

// Modal management
function isModalOpen() {
    return document.querySelector('.modal[style*="display: flex"]') !== null;
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
}

// Mining state management
let miningInProgress = false;

function isMining() {
    return miningInProgress;
}

function setMiningState(state) {
    miningInProgress = !state;
    
    // Update UI elements
    const mineButtons = document.querySelectorAll('.mine-button, .nav-item.mine-btn');
    mineButtons.forEach(btn => {
        btn.style.opacity = state ? '1' : '0.6';
        btn.style.pointerEvents = state ? 'auto' : 'none';
    });
}

// Stats caching
function getCachedStats() {
    const cached = localStorage.getItem('ai_income_stats');
    return cached ? JSON.parse(cached) : null;
}

function cacheStats(stats) {
    stats.cached_at = Date.now();
    localStorage.setItem('ai_income_stats', JSON.stringify(stats));
}

function isCacheValid() {
    const cached = getCachedStats();
    if (!cached || !cached.cached_at) return false;
    
    const cacheAge = Date.now() - cached.cached_at;
    return cacheAge < 60000; // 1 minute cache
}

// Package data management
function getPackageData() {
    // This would normally come from the template, but we'll define it here for JS access
    return [
        {"id": 1, "price": 3, "base_power": 30000, "bonus_power": 7500, "total_power": 37500},
        {"id": 2, "price": 5, "base_power": 50000, "bonus_power": 12500, "total_power": 62500},
        {"id": 3, "price": 10, "base_power": 100000, "bonus_power": 25000, "total_power": 125000},
        {"id": 4, "price": 20, "base_power": 200000, "bonus_power": 50000, "total_power": 250000}
    ];
}

// Visual effects
function createConfettiEffect() {
    // Simple confetti implementation
    const colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0'];
    
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                left: ${Math.random() * 100}vw;
                top: -10px;
                z-index: 10000;
                pointer-events: none;
                border-radius: 50%;
            `;
            
            document.body.appendChild(confetti);
            
            confetti.animate([
                { transform: 'translateY(-10px) rotate(0deg)' },
                { transform: `translateY(100vh) rotate(${Math.random() * 360}deg)` }
            ], {
                duration: 3000,
                easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
            }).onfinish = () => confetti.remove();
            
        }, i * 100);
    }
}

function createPowerUpEffect() {
    // Power-up glow effect
    const effect = document.createElement('div');
    effect.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, #FFD700, transparent);
        transform: translate(-50%, -50%);
        z-index: 10000;
        pointer-events: none;
        border-radius: 50%;
    `;
    
    document.body.appendChild(effect);
    
    effect.animate([
        { transform: 'translate(-50%, -50%) scale(0)', opacity: 0 },
        { transform: 'translate(-50%, -50%) scale(2)', opacity: 1 },
        { transform: 'translate(-50%, -50%) scale(4)', opacity: 0 }
    ], {
        duration: 1500,
        easing: 'ease-out'
    }).onfinish = () => effect.remove();
}

// Network status handling
function handleOnlineStatus() {
    showNotification('🌐 Connection restored', 'success');
}

function handleOfflineStatus() {
    showNotification('📶 Connection lost', 'warning');
}

// Visibility change handling
function handleVisibilityChange() {
    if (document.hidden) {
        // Page hidden - pause timers, etc.
        pauseBackgroundTasks();
    } else {
        // Page visible - resume timers, refresh data
        resumeBackgroundTasks();
        refreshPageData();
    }
}

// Background task management
let backgroundTasks = [];

function pauseBackgroundTasks() {
    backgroundTasks.forEach(task => {
        if (task.timer) {
            clearInterval(task.timer);
        }
    });
}

function resumeBackgroundTasks() {
    backgroundTasks.forEach(task => {
        if (task.callback && task.interval) {
            task.timer = setInterval(task.callback, task.interval);
        }
    });
}

// Stats auto-refresh
function startStatsRefresh() {
    const task = {
        callback: updateStats,
        interval: 30000, // 30 seconds
        timer: setInterval(updateStats, 30000)
    };
    
    backgroundTasks.push(task);
}

async function updateStats() {
    try {
        const result = await apiRequest('/api/stats');
        if (!result.error) {
            // Update UI elements silently
            updateStatsUI(result);
        }
    } catch (error) {
        // Silent fail for background updates
        console.log('Background stats update failed:', error);
    }
}

function updateStatsUI(stats) {
    // Update balance in header
    const balanceElement = document.querySelector('.user-balance span');
    if (balanceElement) {
        balanceElement.textContent = `$${stats.usdt_value.toFixed(2)}`;
    }
    
    // Update stat cards if present
    const hashElement = document.querySelector('.stat-card.success .stat-value');
    if (hashElement) {
        hashElement.textContent = stats.total_hashes.toFixed(6);
    }
    
    const usdtElement = document.querySelector('.stat-card.warning .stat-value');
    if (usdtElement) {
        usdtElement.textContent = `$${stats.usdt_value.toFixed(2)}`;
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--primary-color);
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease;
    `;
    
    if (type === 'success') notification.style.background = 'var(--success-color)';
    if (type === 'warning') notification.style.background = 'var(--warning-color)';
    if (type === 'error') notification.style.background = 'var(--error-color)';
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Page refresh handling
function refreshPageData() {
    const currentPage = getCurrentPage();
    
    switch (currentPage) {
        case 'dashboard':
            updateStats();
            break;
        case 'shop':
            // Refresh shop data if needed
            break;
    }
}

// Additional utility functions for specific features
function shareStats() {
    if (tg?.shareUrl) {
        tg.shareUrl('https://t.me/AI_IncomeBot', 'Check out my AI INCOME mining progress! 🚀');
    } else {
        showNotification('Share feature available in Telegram', 'info');
    }
}

function exportStats() {
    showNotification('Export feature coming soon!', 'info');
}

// Initialize mining tracking
function initializeMiningTracking() {
    // Track mining attempts for analytics
    const miningAttempts = localStorage.getItem('mining_attempts') || 0;
    localStorage.setItem('mining_attempts', parseInt(miningAttempts) + 1);
}

// Animate achievements
function animateAchievements() {
    const achievements = document.querySelectorAll('.achievement-item.unlocked');
    
    achievements.forEach((achievement, index) => {
        setTimeout(() => {
            achievement.style.animation = 'slideInLeft 0.5s ease forwards';
        }, index * 200);
    });
}

// Daily bonus timer
function startDailyBonusTimer() {
    // This would normally calculate real time until next bonus
    const dailyBtn = document.querySelector('.daily-card button');
    if (dailyBtn) {
        // Mock countdown
        let hours = 12, minutes = 34;
        
        const countdown = setInterval(() => {
            if (minutes > 0) {
                minutes--;
            } else if (hours > 0) {
                hours--;
                minutes = 59;
            } else {
                clearInterval(countdown);
                dailyBtn.textContent = '🎁 Claim Bonus';
                dailyBtn.disabled = false;
            }
            
            dailyBtn.innerHTML = `<i class="fas fa-clock"></i> Next bonus in ${hours}h ${minutes}m`;
        }, 60000); // Update every minute
    }
}

// Update Telegram Web App data
function updateTelegramData(result) {
    if (tg?.sendData) {
        tg.sendData(JSON.stringify({
            action: 'mining_completed',
            hashes_earned: result.hashes_earned,
            total_hashes: result.total_hashes,
            usdt_value: result.usdt_value
        }));
    }
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    
    if (tg?.showAlert) {
        tg.showAlert('An unexpected error occurred. Please try refreshing the app.');
    }
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(() => {
            const perfData = performance.timing;
            const loadTime = perfData.loadEventEnd - perfData.navigationStart;
            
            if (loadTime > 5000) {
                console.warn('Slow page load detected:', loadTime + 'ms');
            }
        }, 0);
    });
}