// ===== JARVIS INIT — Boots all components =====
document.addEventListener('DOMContentLoaded', () => {
  // Boot terminal
  setTimeout(bootSequence, 200);

  // Render app grid
  renderApps();

  // Render tasks
  renderTasks();

  // Animate stat bars randomly to simulate live system
  setInterval(() => {
    animateStat('cpuBar', 'cpuVal', 15, 80);
    animateStat('ramBar', 'ramVal', 40, 75);
    animateStat('netBar', 'netVal', 20, 95);
    animateStat('aiBar',  'aiVal',  70, 99);
  }, 3000);

  // Initial Jarvis greeting
  setTimeout(() => {
    jarvisSpeak("All systems are operational, sir. I'm ready to manage your life.", 'greeting');
  }, 2000);

  // Focus terminal input
  setTimeout(() => {
    const input = document.getElementById('cmdInput');
    if (input) input.focus();
  }, 1500);
});

function animateStat(barId, valId, min, max) {
  const val = Math.floor(min + Math.random() * (max - min));
  const bar = document.getElementById(barId);
  const label = document.getElementById(valId);
  if (bar) bar.style.width = val + '%';
  if (label) label.textContent = val + '%';
}
