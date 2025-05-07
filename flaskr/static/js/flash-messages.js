// Handle form submissions
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Show loading message immediately
            const loadingMessage = document.createElement('div');
            loadingMessage.className = 'flash-message loading';
            loadingMessage.textContent = 'Searching...';
            loadingMessage.style.opacity = '0';
            
            const flashContainer = document.querySelector('.flash-messages') || 
                                 createFlashContainer();
            flashContainer.appendChild(loadingMessage);
            
            // Force a reflow to ensure animation plays
            loadingMessage.offsetHeight;
            loadingMessage.style.opacity = '1';
        });
    });
});

// Handle existing flash messages
function handleFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        const category = message.dataset.category;
        
        // Auto-dismiss loading messages when results are shown
        if (category === 'loading') {
            const resultsContainer = document.querySelector('.pokemon-data-container, .type-data-container');
            if (resultsContainer && resultsContainer.children.length > 0) {
                message.classList.add('fade-out');
                setTimeout(() => message.remove(), 300);
            }
        }
        
        // Auto-dismiss info messages after 3 seconds
        if (category === 'info') {
            setTimeout(() => {
                message.classList.add('fade-out');
                setTimeout(() => message.remove(), 300);
            }, 3000);
        }
        
        // Keep error messages visible until next action
        if (category === 'error') {
            message.addEventListener('click', () => {
                message.classList.add('fade-out');
                setTimeout(() => message.remove(), 300);
            });
        }
    });
}

// Create flash container if it doesn't exist
function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.insertBefore(container, document.body.firstChild);
    return container;
}

// Run on page load
document.addEventListener('DOMContentLoaded', handleFlashMessages); 