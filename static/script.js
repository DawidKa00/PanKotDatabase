// Funkcja do przełączania trybu ciemnego
document.addEventListener('DOMContentLoaded', function() {
  const toggleButton = document.getElementById('toggle-dark-mode');
  if (!toggleButton) return; // Zakończ, jeśli nie ma przycisku na stronie

  const currentTheme = localStorage.getItem('theme');

  // Ustawienie początkowego trybu na podstawie zapisanej wartości
  if (currentTheme === 'dark') {
    document.body.classList.add('dark-mode');
    updateTableThemes('dark');
    updateColors('dark');
  } else {
    updateTableThemes('light');
    updateColors('light');
  }

  // Ustaw początkowy wygląd przycisku
  toggleButton.innerHTML = document.body.classList.contains('dark-mode')
    ? '<i class="bi bi-sun-fill"></i> Tryb Jasny'
    : '<i class="bi bi-moon-fill"></i> Tryb Ciemny';

  toggleButton.addEventListener('click', () => {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    const newTheme = isDarkMode ? 'dark' : 'light';
    localStorage.setItem('theme', newTheme);  // Zapisanie preferencji w localStorage

    // Zmiana ikony przycisku
    toggleButton.innerHTML = isDarkMode
      ? '<i class="bi bi-sun-fill"></i> Tryb Jasny'
      : '<i class="bi bi-moon-fill"></i> Tryb Ciemny';

    // Aktualizacja wszystkich tabel i tytułów
    updateTableThemes(newTheme);
    updateColors(newTheme);
  });
});

// Funkcja do zmiany klas wszystkich tabel w zależności od trybu
function updateTableThemes(theme) {
  const tables = document.querySelectorAll('table');
  if (tables.length === 0) return; // Nie rób nic jeśli nie ma tabel

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

// Funkcja do zmiany koloru wszystkich tytułów h1
function updateColors(theme) {
  const titles = document.querySelectorAll('h1');

  if (titles.length === 0) return; // Nie rób nic jeśli nie ma tytułów h1

  titles.forEach(title => {
    if (theme === 'dark') {
      title.style.color = '#ffffff'; // Biały w trybie ciemnym
    } else {
      title.style.color = '#212529'; // Czarny w trybie jasnym
    }
  });

  const span = document.querySelectorAll('span');

  if (span.length === 0) return;

  span.forEach(span => {
    if (theme === 'dark') {
      span.style.color = '#ffffff'; // Biały w trybie ciemnym
    } else {
      span.style.color = '#212529'; // Czarny w trybie jasnym
    }
  });
}