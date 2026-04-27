// ===== ACTIVITY LOGGER COMPONENT =====
function addLog(type, tag, msg) {
  const feed = document.getElementById('logFeed');
  if (!feed) return;

  const now = new Date();
  const ts = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}:${String(now.getSeconds()).padStart(2,'0')}`;

  const entry = document.createElement('div');
  entry.className = 'log-entry';
  entry.innerHTML = `
    <span class="log-time">[${ts}]</span>
    <span class="log-tag ${type}">${tag}</span>
    <span class="log-msg">${msg}</span>
  `;
  feed.appendChild(entry);

  // Keep max 50 entries
  while (feed.children.length > 50) feed.removeChild(feed.firstChild);

  feed.scrollTop = feed.scrollHeight;
}

// Ambient log events to simulate Jarvis activity
const ambientEvents = [
  ['info', 'SYS',    'Heartbeat check — all systems nominal'],
  ['info', 'NET',    'Network latency: 12ms'],
  ['action','AI',   'Processing background task queue'],
  ['info', 'SYS',   'RAM usage optimized — freed 0.4 GB'],
  ['ok',   'SEC',   'Firewall rules updated'],
  ['info', 'SYS',   'Screen brightness adjusted (auto)'],
  ['action','AI',   'Analyzing usage patterns'],
  ['info', 'NET',   'Discord voice latency: 18ms'],
  ['ok',   'AI',    'Prediction model updated'],
  ['info', 'SYS',   'CPU throttle inactive — performance mode ON'],
];

let ambientIdx = 0;
function emitAmbientLog() {
  const e = ambientEvents[ambientIdx % ambientEvents.length];
  addLog(e[0], e[1], e[2]);
  ambientIdx++;
  setTimeout(emitAmbientLog, 4000 + Math.random() * 4000);
}

// Initial logs
const initLogs = [
  ['ok',   'BOOT', 'JARVIS neural core initialized'],
  ['ok',   'BOOT', 'All subsystems online'],
  ['info', 'AUTH', 'User identity confirmed — Welcome, sir'],
];

initLogs.forEach((l, i) => setTimeout(() => addLog(l[0], l[1], l[2]), i * 300));
setTimeout(emitAmbientLog, 3000);
