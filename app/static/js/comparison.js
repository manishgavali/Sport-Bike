document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('comparisonForm');
    const checkboxes = document.querySelectorAll('.bike-checkbox');
    const cards = document.querySelectorAll('.bike-card');
    
    // Add visual feedback for checkbox selection
    checkboxes.forEach(function(checkbox) {
        const card = checkbox.closest('.bike-card');
        
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                card.style.border = '2px solid var(--accent-cyan)';
                card.style.boxShadow = '0 0 20px rgba(0, 217, 255, 0.5)';
                card.style.transform = 'scale(1.02)';
            } else {
                card.style.border = '1px solid rgba(255, 255, 255, 0.1)';
                card.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.3)';
                card.style.transform = 'scale(1)';
            }
        });
    });
    
    // Form validation
    form.addEventListener('submit', function(e) {
        const checkedBoxes = document.querySelectorAll('.bike-checkbox:checked');
        
        if (checkedBoxes.length < 2) {
            e.preventDefault();
            alert('Please select at least 2 bikes to compare');
            return false;
        }
        
        if (checkedBoxes.length > 5) {
            e.preventDefault();
            alert('You can compare maximum 5 bikes at once');
            return false;
        }
    });
});
