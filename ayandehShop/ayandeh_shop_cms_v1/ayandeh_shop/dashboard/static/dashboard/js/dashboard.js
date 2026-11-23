(function () {
  const body = document.querySelector('.cms-body');
  const themeButton = document.getElementById('cmsThemeToggle');
  const sidebar = document.getElementById('cmsSidebar');
  const menuButton = document.getElementById('cmsMenuToggle');
  const backdrop = document.getElementById('cmsSidebarBackdrop');

  function setTheme(theme) {
    if (!body) return;
    body.dataset.theme = theme;
    try { localStorage.setItem('ayandeh-cms-theme', theme); } catch (error) { /* Storage may be disabled. */ }
    if (themeButton) {
      themeButton.innerHTML = theme === 'dark'
        ? '<i class="bi bi-sun"></i>'
        : '<i class="bi bi-moon-stars"></i>';
    }
  }

  let savedTheme = 'light';
  try { savedTheme = localStorage.getItem('ayandeh-cms-theme') || 'light'; } catch (error) { /* Keep light theme. */ }
  setTheme(savedTheme === 'dark' ? 'dark' : 'light');

  if (themeButton) {
    themeButton.addEventListener('click', function () {
      setTheme(body.dataset.theme === 'dark' ? 'light' : 'dark');
    });
  }

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('open');
    if (backdrop) backdrop.classList.remove('show');
  }
  if (menuButton) menuButton.addEventListener('click', function () {
    sidebar.classList.toggle('open');
    backdrop.classList.toggle('show');
  });
  if (backdrop) backdrop.addEventListener('click', closeSidebar);

  document.querySelectorAll('form[data-confirm]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
  });
})();
