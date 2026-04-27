// ===== APP LAUNCHER COMPONENT =====
const APPS = [
  { id: 'obs',      name: 'OBS Studio',   icon: '🎬', status: 'idle' },
  { id: 'steam',    name: 'Steam',        icon: '🎮', status: 'idle' },
  { id: 'youtube',  name: 'YouTube',      icon: '▶️',  status: 'idle' },
  { id: 'twitch',   name: 'Twitch',       icon: '📡', status: 'idle' },
  { id: 'discord',  name: 'Discord',      icon: '💬', status: 'idle' },
  { id: 'chrome',   name: 'Chrome',       icon: '🌐', status: 'idle' },
  { id: 'vscode',   name: 'VS Code',      icon: '💻', status: 'idle' },
  { id: 'spotify',  name: 'Spotify',      icon: '🎵', status: 'idle' },
  { id: 'notion',   name: 'Notion',       icon: '📋', status: 'idle' },
];

const appStates = {};
APPS.forEach(a => appStates[a.id] = false);

function renderApps() {
  const grid = document.getElementById('appGrid');
  if (!grid) return;
  grid.innerHTML = '';
  APPS.forEach(app => {
    const card = document.createElement('div');
    card.className = `app-card${appStates[app.id] ? ' active' : ''}`;
    card.id = `app-${app.id}`;
    card.innerHTML = `
      <div class="app-icon">${app.icon}</div>
      <div class="app-name">${app.name}</div>
      <div class="app-status">${appStates[app.id] ? 'RUNNING' : 'IDLE'}</div>
    `;
    card.addEventListener('click', () => launchApp(app));
    grid.appendChild(card);
  });
}

function launchApp(app) {
  const wasActive = appStates[app.id];
  appStates[app.id] = !wasActive;
  renderApps();

  const action = wasActive ? 'closed' : 'launched';
  const logType = wasActive ? 'warn' : 'ok';
  addLog(logType, `APP`, `${app.name} ${action}`);

  if (!wasActive) {
    setCoreStatus('ACTIVE', 'active');
    jarvisSpeak(`${app.name} has been ${action}, sir.`);
    printLine(`${app.name} ${action} by JARVIS.`, 'res');
    setTimeout(() => setCoreStatus('STANDBY', ''), 2000);
  }
}

function toggleApp(id, active) {
  appStates[id] = active;
  renderApps();
}

function setCoreStatus(text, cls) {
  const el = document.getElementById('coreStatus');
  if (!el) return;
  el.textContent = text;
  el.className = `core-status${cls ? ' ' + cls : ''}`;
}
