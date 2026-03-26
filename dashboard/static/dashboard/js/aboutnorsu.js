/**
 * About NORSU Page JavaScript
 * Handles dynamic loading of NORSU information from localStorage
 * Connected to Super Admin Dashboard's NORSU Information Management
 */

class NORSUAboutPage {
    constructor() {
        this.storageKey = 'superAdminNORSUInfo';
        this.presidentStorageKey = 'superAdminPresidentInfo';
        this.historyStorageKey = 'superAdminHistoryInfo';
        this.contentArea = null;
        this.refreshInterval = null;
        this.navEl = null;
        this.lastUpdatedEl = null;
        this.observer = null;
        this.init();
    }

    /**
     * Initialize the About NORSU page
     */
    init() {
        console.log('About NORSU page initialized');
        this.contentArea = document.getElementById('contentArea');
        this.navEl = document.getElementById('aboutNav');
        this.lastUpdatedEl = document.getElementById('aboutLastUpdated');
        
        if (this.contentArea) {
            this.loadNORSUInformation();
            this.applyPresidentProfile();
            this.applyHistorySection();
            this.setupActions();
            this.setupSectionNav();
            // Keep auto-refresh, but avoid being too aggressive.
            this.setupAutoRefresh();
            this.setupStorageListener();
            this.setupKeyboardShortcuts();
        } else {
            console.error('Content area not found');
        }
    }

    setupActions() {
        const refreshBtn = document.getElementById('aboutRefreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.loadNORSUInformation());
        }

        const copyBtn = document.getElementById('aboutCopyLinkBtn');
        if (copyBtn) {
            copyBtn.addEventListener('click', async () => {
                const url = window.location.href;
                try {
                    if (navigator.clipboard?.writeText) {
                        await navigator.clipboard.writeText(url);
                    } else {
                        const temp = document.createElement('textarea');
                        temp.value = url;
                        document.body.appendChild(temp);
                        temp.select();
                        document.execCommand('copy');
                        temp.remove();
                    }
                    copyBtn.blur();
                } catch (e) {
                    console.warn('Copy failed:', e);
                }
            });
        }

        // Smooth scrolling for pills
        if (this.navEl) {
            this.navEl.addEventListener('click', (e) => {
                const a = e.target.closest('a[href^="#"]');
                if (!a) return;
                const id = a.getAttribute('href');
                const el = document.querySelector(id);
                if (!el) return;
                e.preventDefault();
                el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
        }
    }

    /**
     * Load NORSU information from localStorage
     */
    async loadNORSUInformation() {
        if (!this.contentArea) return;

        try {
            this.showLoadingState();

            // Get data from localStorage (same key used in super admin dashboard)
            const infoData = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
            
            // Simulate loading delay for better UX
            await this.delay(450);

            if (infoData.length === 0) {
                this.showNoDataState();
            } else {
                // Get the most recent entry (last item in array)
                const latestInfo = infoData[infoData.length - 1];
                this.displayNORSUInfo(latestInfo);
            }

        } catch (error) {
            console.error('Error loading NORSU information:', error);
            this.showErrorState();
        }
    }

    /**
     * Display loading state
     */
    showLoadingState() {
        // If the template already has section cards, just set placeholders.
        const fields = this.contentArea.querySelectorAll('[data-field]');
        if (fields.length > 0) {
            fields.forEach(el => (el.textContent = 'Loading…'));
        } else {
            this.contentArea.innerHTML = `
                <div class="loading">
                    <i class="fas fa-spinner fa-spin"></i>
                    <h2>Loading NORSU Information...</h2>
                    <p>Please wait while we fetch the latest information.</p>
                </div>
            `;
        }

        if (this.lastUpdatedEl) {
            this.lastUpdatedEl.hidden = true;
            this.lastUpdatedEl.textContent = '';
        }
    }

    /**
     * Display NORSU information
     */
    displayNORSUInfo(info) {
        if (!this.contentArea || !info) return;
        
        console.log('Received info object:', info);
        console.log('Strategic Goals from info:', info.strategicGoals);

        // Format Strategic Goals - display as plain text
        const formatStrategicGoals = (text) => {
            console.log('Original Strategic Goals text:', text);
            
            if (!text || text === 'Strategic goals are not available yet.') {
                return text;
            }
            
            // Just return the text as-is with proper line breaks
            const result = text.replace(/\n/g, '<br>');
            console.log('Final Strategic Goals result:', result);
            return result;
        };

        // Format Core Values - display as plain text
        const formatCoreValues = (text) => {
            console.log('Original Core Values text:', text);
            
            if (!text || text === 'Core values are not available yet.') {
                return text;
            }
            
            // Just return the text as-is with proper line breaks
            const result = text.replace(/\n/g, '<br>');
            console.log('Final Core Values result:', result);
            return result;
        };

        const data = {
            generalMandate: info.generalMandate || 'No general mandate available yet.',
            vision: info.vision || 'No vision statement available yet.',
            mission: info.mission || 'No mission statement available yet.',
            strategicGoals: formatStrategicGoals(info.strategicGoals),
            coreValues: formatCoreValues(info.coreValues),
            qualityPolicy: info.qualityPolicy || 'No quality policy available yet.'
        };

        const fields = this.contentArea.querySelectorAll('[data-field]');
        if (fields.length > 0) {
            fields.forEach(el => {
                const key = el.getAttribute('data-field');
                if (!key) return;
                
                if (key === 'strategicGoals' || key === 'coreValues') {
                    // Use innerHTML for Strategic Goals and Core Values to preserve formatting
                    el.innerHTML = data[key] || '';
                } else {
                    // Use textContent for other fields to prevent HTML injection
                    el.textContent = data[key] ?? '';
                }
            });
        } else {
            // Fallback for older markup if this template gets swapped.
            this.contentArea.innerHTML = `
                <div class="error-state">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h2>Page needs an update</h2>
                    <p>The About page template was updated but could not be detected. Please refresh.</p>
                    <button class="refresh-btn" onclick="window.location.reload()">Reload</button>
                </div>
            `;
        }

        if (this.lastUpdatedEl) {
            const when = info.createdDate ? new Date(info.createdDate).toLocaleString() : 'Unknown';
            this.lastUpdatedEl.hidden = false;
            this.lastUpdatedEl.innerHTML = `<i class="fa-solid fa-clock"></i> Last updated: <strong>${this.escapeHtml(String(when))}</strong>`;
        }
    }

    /**
     * Show no data state
     */
    showNoDataState() {
        if (!this.contentArea) return;

        const fields = this.contentArea.querySelectorAll('[data-field]');
        if (fields.length > 0) {
            // Show friendly default content so the page isn't empty.
            const defaults = {
                mission: 'To provide quality and inclusive education, foster research and innovation, and deliver responsive community extension services.',
                vision: 'A globally competitive state university producing competent, values-driven, and service-oriented graduates.',
                qualityPolicy: 'We commit to continually improve our services and meet stakeholder requirements through an effective quality management system.',
                strategicGoals: 'Strengthen instruction, accelerate research and innovation, expand extension services, and enhance institutional governance and partnerships.',
                coreValues: 'Integrity • Excellence • Service • Innovation • Accountability',
                history: 'Institutional history will appear here once published by the administrator.'
            };
            fields.forEach(el => {
                const key = el.getAttribute('data-field');
                el.textContent = defaults[key] || '';
            });
        } else {
            this.contentArea.innerHTML = `
                <div class="error-state">
                    <i class="fas fa-info-circle"></i>
                    <h2>No Information Available</h2>
                    <p>NORSU information has not been added yet. Please contact the administrator to update the institutional information.</p>
                    <button class="refresh-btn" onclick="window.norsuAboutPage.loadNORSUInformation()">
                        <i class="fas fa-sync-alt"></i> Refresh
                    </button>
                </div>
            `;
        }

        if (this.lastUpdatedEl) {
            this.lastUpdatedEl.hidden = false;
            this.lastUpdatedEl.innerHTML = `<i class="fa-solid fa-circle-info"></i> Showing default content (admin data not yet published).`;
        }
    }

    /**
     * Show error state
     */
    showErrorState() {
        if (!this.contentArea) return;

        this.contentArea.innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-triangle"></i>
                <h2>Unable to Load Information</h2>
                <p>We encountered an error while loading the NORSU information. Please try again.</p>
                <button class="refresh-btn" onclick="window.norsuAboutPage.loadNORSUInformation()">
                    <i class="fas fa-sync-alt"></i> Try Again
                </button>
            </div>
        `;

        if (this.lastUpdatedEl) {
            this.lastUpdatedEl.hidden = true;
            this.lastUpdatedEl.textContent = '';
        }
    }

    /**
     * Setup auto-refresh functionality
     */
    setupAutoRefresh() {
        // Check for updates periodically (avoid overly frequent refresh).
        this.refreshInterval = setInterval(() => {
            this.loadNORSUInformation();
        }, 120000);
    }

    /**
     * Setup storage event listener for cross-tab updates
     */
    setupStorageListener() {
        window.addEventListener('storage', (e) => {
            if (e.key === this.storageKey) {
                console.log('NORSU information updated in another tab, refreshing...');
                this.loadNORSUInformation();
            }
            if (e.key === this.presidentStorageKey) {
                console.log('President profile updated in another tab, refreshing...');
                this.applyPresidentProfile();
            }
            if (e.key === this.historyStorageKey) {
                console.log('History info updated in another tab, refreshing...');
                this.applyHistorySection();
            }
        });
    }

    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+R or F5 to refresh
            if ((e.ctrlKey && e.key === 'r') || e.key === 'F5') {
                e.preventDefault();
                this.loadNORSUInformation();
            }
            // Escape to stop auto-refresh
            if (e.key === 'Escape') {
                this.stopAutoRefresh();
            }
        });
    }

    /**
     * Stop auto-refresh
     */
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
            console.log('Auto-refresh stopped');
        }
    }

    setupSectionNav() {
        if (!this.navEl) return;

        const pills = Array.from(this.navEl.querySelectorAll('a[href^="#"]'));
        const targets = pills
            .map(a => document.querySelector(a.getAttribute('href')))
            .filter(Boolean);

        if (targets.length === 0) return;

        const setActive = (id) => {
            pills.forEach(a => {
                const href = a.getAttribute('href');
                a.classList.toggle('active', href === id);
            });
        };

        // Initial state
        setActive(pills[0]?.getAttribute('href') || '#mission');

        try {
            this.observer = new IntersectionObserver((entries) => {
                const visible = entries
                    .filter(e => e.isIntersecting)
                    .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
                if (visible?.target?.id) {
                    setActive(`#${visible.target.id}`);
                }
            }, { root: null, threshold: [0.25, 0.4, 0.6], rootMargin: '-20% 0px -65% 0px' });

            targets.forEach(t => this.observer.observe(t));
        } catch (e) {
            console.warn('IntersectionObserver not available:', e);
        }
    }

    /**
     * Restart auto-refresh
     */
    restartAutoRefresh() {
        this.stopAutoRefresh();
        this.setupAutoRefresh();
        console.log('Auto-refresh restarted');
    }

    /**
     * Apply University President profile from localStorage to the About page section
     */
    applyPresidentProfile() {
        const imgEl = document.getElementById('presidentPhotoImg');
        const roleEl = document.getElementById('presidentRole');
        const nameEl = document.getElementById('presidentName');
        const captionEl = document.getElementById('presidentCaption');

        if (!imgEl && !roleEl && !nameEl && !captionEl) {
            return;
        }

        let data = null;
        try {
            const raw = localStorage.getItem(this.presidentStorageKey);
            data = raw ? JSON.parse(raw) : null;
        } catch (e) {
            console.warn('Invalid president profile data on About page:', e);
        }

        if (!data) return;

        if (data.role && roleEl) {
            roleEl.textContent = data.role;
        }
        if (data.name && nameEl) {
            nameEl.textContent = data.name;
        }
        if (data.caption && captionEl) {
            captionEl.textContent = data.caption;
        }
        if (data.photo && imgEl) {
            imgEl.src = data.photo;
        }
    }

    /**
     * Apply NORSU History text from localStorage to the About page section
     */
    applyHistorySection() {
        const section = document.getElementById('norsu-history');
        if (!section) return;

        const titleEl = section.querySelector('.history-left h2');
        const subtitleEl = section.querySelector('.history-left p');
        const bodyContainer = section.querySelector('.history-right');

        let data = null;
        try {
            const raw = localStorage.getItem(this.historyStorageKey);
            data = raw ? JSON.parse(raw) : null;
        } catch (e) {
            console.warn('Invalid history data on About page:', e);
        }

        if (!data) return;

        if (titleEl && data.title) {
            titleEl.textContent = data.title;
        }
        if (subtitleEl && data.subtitle) {
            subtitleEl.textContent = data.subtitle;
        }
        if (bodyContainer && data.body) {
            // Replace content paragraphs with a single block of text, preserving line breaks
            bodyContainer.innerHTML = '';
            const p = document.createElement('p');
            p.style.whiteSpace = 'pre-line';
            p.textContent = data.body;
            bodyContainer.appendChild(p);
        }
    }

    /**
     * Utility function to escape HTML
     */
    escapeHtml(text) {
        if (!text) return '';
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    /**
     * Utility function to create delay
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Get information count from localStorage
     */
    getInfoCount() {
        try {
            const infoData = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
            return infoData.length;
        } catch (error) {
            console.error('Error getting info count:', error);
            return 0;
        }
    }

    /**
     * Get latest information without displaying
     */
    getLatestInfo() {
        try {
            const infoData = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
            return infoData.length > 0 ? infoData[infoData.length - 1] : null;
        } catch (error) {
            console.error('Error getting latest info:', error);
            return null;
        }
    }

    /**
     * Export data for backup
     */
    exportData() {
        try {
            const infoData = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
            const dataStr = JSON.stringify(infoData, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);
            
            const link = document.createElement('a');
            link.href = url;
            link.download = `norsu_info_backup_${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            
            URL.revokeObjectURL(url);
            console.log('Data exported successfully');
        } catch (error) {
            console.error('Error exporting data:', error);
        }
    }

    /**
     * Cleanup method
     */
    destroy() {
        this.stopAutoRefresh();
        if (this.observer) {
            this.observer.disconnect();
            this.observer = null;
        }
        console.log('About NORSU page destroyed');
    }
}

// Global functions for backward compatibility
window.loadNORSUInformation = function() {
    if (window.norsuAboutPage) {
        window.norsuAboutPage.loadNORSUInformation();
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.norsuAboutPage = new NORSUAboutPage();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.norsuAboutPage) {
        window.norsuAboutPage.destroy();
    }
});
