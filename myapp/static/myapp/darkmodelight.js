document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('theme-toggle');
    const html = document.documentElement;

    // Set initial theme
    const currentTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', currentTheme);
    toggle.checked = currentTheme === 'dark';

    // Toggle handler
    toggle.addEventListener('change', function() {
        const newTheme = this.checked ? 'dark' : 'light';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        // Debug log
        console.log('Theme changed to:', newTheme);
    });
});