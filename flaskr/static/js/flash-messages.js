// Handle form submissions
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Show loading message inside the pokedex
            const statusDiv = document.getElementById('search-status-message');
            if (statusDiv) {
                statusDiv.innerHTML = '<p class="loading-message">Searching...</p>';
            }
        });
    });
});

// Remove flash message handling for loading/info/error
// Instead, clear the loading message when results are rendered
function clearSearchStatusIfResults() {
    const statusDiv = document.getElementById('search-status-message');
    const resultsContainer = document.querySelector('.pokemon-data-container, .type-data-container');
    if (statusDiv && resultsContainer && resultsContainer.children.length > 0) {
        statusDiv.innerHTML = '';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    clearSearchStatusIfResults();
});

document.addEventListener('readystatechange', function() {
    if (document.readyState === 'complete') {
        clearSearchStatusIfResults();
    }
});

// Create flash container if it doesn't exist
function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.insertBefore(container, document.body.firstChild);
    return container;
}

// Run on page load
document.addEventListener('DOMContentLoaded', handleFlashMessages); 