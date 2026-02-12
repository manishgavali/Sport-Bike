// Form validation utilities

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    const hasLength = password.length >= 8;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    
    return hasLength && hasUpper && hasLower && hasNumber;
}

function validatePhone(phone) {
    const re = /^[6-9]\d{9}$/;
    return re.test(phone);
}

function showError(input, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.color = 'var(--accent-orange)';
    errorDiv.style.fontSize = '0.85rem';
    errorDiv.style.marginTop = '0.5rem';
    errorDiv.textContent = message;
    
    // Remove existing error
    const existingError = input.parentElement.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    input.parentElement.appendChild(errorDiv);
    input.style.borderColor = 'var(--accent-orange)';
}

function clearError(input) {
    const errorDiv = input.parentElement.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.remove();
    }
    input.style.borderColor = 'rgba(255, 255, 255, 0.1)';
}

// Real-time validation
document.addEventListener('DOMContentLoaded', function() {
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value && !validateEmail(this.value)) {
                showError(this, 'Please enter a valid email address');
            } else {
                clearError(this);
            }
        });
    });
    
    // Password validation
    const passwordInputs = document.querySelectorAll('input[name="password"]');
    passwordInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value && !validatePassword(this.value)) {
                showError(this, 'Password must be 8+ characters with uppercase, lowercase, and number');
            } else {
                clearError(this);
            }
        });
    });
});
