// ===== CLOCK UTILITY =====
function updateClock() {
  const now = new Date();
  const hh = String(now.getHours()).padStart(2, '0');
  const mm = String(now.getMinutes()).padStart(2, '0');
  const ss = String(now.getSeconds()).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');
  const mo = String(now.getMonth() + 1).padStart(2, '0');
  const yy = now.getFullYear();

  const clockEl = document.getElementById('clock');
  const dateEl = document.getElementById('date');
  if (clockEl) clockEl.textContent = `${hh}:${mm}:${ss}`;
  if (dateEl) dateEl.textContent = `${yy}/${mo}/${dd}`;
}

setInterval(updateClock, 1000);
updateClock();
