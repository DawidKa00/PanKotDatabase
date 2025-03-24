document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('toggle-dark-mode');
    if (!toggleButton) return;
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
        updateTableThemes('dark');
        updateColors('dark');
    } else {
        updateTableThemes('light');
        updateColors('light');
    }

    toggleButton.innerHTML = document.body.classList.contains('dark-mode')
        ? '<i class="bi bi-sun-fill"></i>'
        : '<i class="bi bi-moon-fill"></i>';

    toggleButton.addEventListener('click', () => {
        const isDarkMode = document.body.classList.toggle('dark-mode');
        const newTheme = isDarkMode ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);

        toggleButton.innerHTML = isDarkMode
            ? '<i class="bi bi-sun-fill"></i>'
            : '<i class="bi bi-moon-fill"></i>';

        updateTableThemes(newTheme);
        updateColors(newTheme);
    });
});

function updateTableThemes(theme) {
    const tables = document.querySelectorAll('table');
    if (tables.length === 0) return;

    tables.forEach(table => {
        if (theme === 'dark') {
            table.classList.remove('table-light');
            table.classList.add('table-dark');
        } else {
            table.classList.remove('table-dark');
            table.classList.add('table-light');
        }
    });
}

function updateColors(theme) {
    const titles = document.querySelectorAll('h1, span');
    if (titles.length === 0) return;

    titles.forEach(title => {
        title.style.color = theme === 'dark' ? '#ffffff' : '#212529';
    });
}