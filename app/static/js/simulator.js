document.addEventListener('DOMContentLoaded', function() {
    const simulatorForm = document.querySelector('form');
    
    if (simulatorForm) {
        // Add loading animation on submit
        simulatorForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.textContent = 'Simulating...';
            submitBtn.disabled = true;
        });
        
        // Real-time weight adjustment display
        const weightInput = document.querySelector('input[name="rider_weight"]');
        if (weightInput) {
            weightInput.addEventListener('input', function() {
                const value = this.value;
                const label = this.previousElementSibling;
                label.textContent = `Rider Weight (${value} kg)`;
            });
        }
    }
});

// Animate result cards on results page
window.addEventListener('load', function() {
    const resultCards = document.querySelectorAll('.result-card');
    resultCards.forEach(function(card, index) {
        setTimeout(function() {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.5s ease';
            
            setTimeout(function() {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        }, index * 100);
    });
});
