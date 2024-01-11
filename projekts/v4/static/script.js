document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('menuForm');
    const loadingScreen = document.getElementById('loadingScreen');

    form.addEventListener('submit', function(event) {
        // Show the loading screen
        loadingScreen.classList.remove('loading-hidden');

        // Optional: Add a slight delay before form submission
        setTimeout(function() {
            form.submit();
        }, 100); // Delay in milliseconds
    });
});
