// Main JavaScript utilities for the Review Platform

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        console.error('Error:', message);
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }
}

/**
 * Show success message
 * @param {string} message - Success message to display
 */
function showSuccess(message) {
    const successDiv = document.getElementById('successMessage');
    if (successDiv) {
        successDiv.textContent = message;
        successDiv.style.display = 'block';
        console.log('Success:', message);
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            successDiv.style.display = 'none';
        }, 5000);
    }
}

/**
 * Make API call with error handling
 * @param {string} url - API endpoint URL
 * @param {object} options - Fetch options
 * @returns {Promise} Response promise
 */
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || `HTTP Error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error.message);
        throw error;
    }
}

/**
 * Format date to readable format
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Create star rating HTML
 * @param {number} rating - Rating from 1-5
 * @returns {string} HTML star rating
 */
function createStarRating(rating) {
    let stars = '';
    for (let i = 0; i < Math.round(rating); i++) {
        stars += '⭐';
    }
    return stars || '-';
}

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid
 */
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {object} Validation result
 */
function validatePassword(password) {
    const results = {
        length: password.length >= 6,
        hasUpper: /[A-Z]/.test(password),
        hasLower: /[a-z]/.test(password),
        hasNumber: /\d/.test(password),
        isStrong: password.length >= 8
    };
    return results;
}

/**
 * Debounce function for search
 * @param {function} func - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Truncate text to specified length
 * @param {string} text - Text to truncate
 * @param {number} length - Max length
 * @returns {string} Truncated text
 */
function truncateText(text, length = 100) {
    if (text.length > length) {
        return text.substring(0, length) + '...';
    }
    return text;
}

/**
 * Get query parameter from URL
 * @param {string} param - Parameter name
 * @returns {string|null} Parameter value
 */
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

/**
 * Clear form fields
 * @param {string} formId - Form element ID
 */
function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

/**
 * Check if user is on mobile
 * @returns {boolean} True if mobile device
 */
function isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

/**
 * Local storage helper - save data
 * @param {string} key - Storage key
 * @param {*} value - Value to store
 */
function saveLocal(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
        console.error('Local storage error:', error);
    }
}

/**
 * Local storage helper - retrieve data
 * @param {string} key - Storage key
 * @returns {*} Stored value
 */
function getLocal(key) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (error) {
        console.error('Local storage error:', error);
        return null;
    }
}

/**
 * Local storage helper - remove data
 * @param {string} key - Storage key
 */
function removeLocal(key) {
    try {
        localStorage.removeItem(key);
    } catch (error) {
        console.error('Local storage error:', error);
    }
}

/**
 * Show loading state on button
 * @param {string} buttonId - Button element ID
 * @param {boolean} isLoading - Loading state
 */
function setButtonLoading(buttonId, isLoading) {
    const button = document.getElementById(buttonId);
    if (button) {
        if (isLoading) {
            button.disabled = true;
            button.classList.add('loading');
            button.textContent = 'Loading...';
        } else {
            button.disabled = false;
            button.classList.remove('loading');
            button.textContent = button.dataset.originalText || 'Submit';
        }
    }
}

/**
 * Confirm dialog
 * @param {string} message - Confirmation message
 * @returns {boolean} User confirmation
 */
function confirmAction(message) {
    return confirm(message || 'Are you sure you want to proceed?');
}

// Initialize tooltips (if using Bootstrap or similar)
document.addEventListener('DOMContentLoaded', function() {
    console.log('Review Platform loaded');
    
    // Add any global event listeners here
    // Example: Close messages on click
    document.querySelectorAll('.error-message, .success-message').forEach(msg => {
        msg.addEventListener('click', function() {
            this.style.display = 'none';
        });
    });
});

/**
 * Format currency
 * @param {number} amount - Amount to format
 * @returns {string} Formatted currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

/**
 * Get time ago string
 * @param {Date} date - Date object
 * @returns {string} Time ago string
 */
function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    let interval = seconds / 31536000;
    if (interval > 1) return Math.floor(interval) + ' years ago';
    
    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + ' months ago';
    
    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + ' days ago';
    
    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + ' hours ago';
    
    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + ' minutes ago';
    
    return Math.floor(seconds) + ' seconds ago';
}

/**
 * Smooth scroll to element
 * @param {string} elementId - Element ID to scroll to
 */
function smoothScroll(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Toggle visibility of element
 * @param {string} elementId - Element ID to toggle
 */
function toggleElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = element.style.display === 'none' ? 'block' : 'none';
    }
}

export {
    showError,
    showSuccess,
    apiCall,
    formatDate,
    createStarRating,
    isValidEmail,
    validatePassword,
    debounce,
    truncateText,
    getQueryParam,
    clearForm,
    isMobileDevice,
    saveLocal,
    getLocal,
    removeLocal,
    setButtonLoading,
    confirmAction,
    formatCurrency,
    getTimeAgo,
    smoothScroll,
    toggleElement
};
