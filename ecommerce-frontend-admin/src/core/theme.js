const KEY = 'admin-theme';

function applyTheme(theme) {
  document.documentElement.classList.toggle('dark', theme === 'dark');
}

export function initTheme() {
  applyTheme(localStorage.getItem(KEY) || 'dark');
}

export function toggleTheme() {
  const next = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
  localStorage.setItem(KEY, next);
  applyTheme(next);
  return next;
}

export function isDark() {
  return document.documentElement.classList.contains('dark');
}
