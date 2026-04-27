// ===== TERMINAL COMPONENT =====
const terminalHistory = [];
let historyIndex = -1;

const bootLines = [
  { type: 'info', text: '[ JARVIS SYSTEM BOOT ]' },
  { type: 'info', text: 'Initializing neural networks...' },
  { type: 'res',  text: '> Core AI engine: ONLINE' },
  { type: 'res',  text: '> Voice synthesis: ONLINE' },
  { type: 'res',  text: '> App controller: ONLINE' },
  { type: 'res',  text: '> Task manager: ONLINE' },
  { type: 'warn', text: '> External API: LIMITED (demo mode)' },
  { type: 'info', text: '─────────────────────────────────' },
  { type: 'res',  text: 'System ready. How may I assist, sir?' },
];

function printLine(text, type = 'info') {
  const output = document.getElementById('terminalOutput');
  if (!output) return;
  const div = document.createElement('div');
  div.className = `t-line ${type}`;
  div.textContent = text;
  output.appendChild(div);
  output.scrollTop = output.scrollHeight;
}

function bootSequence() {
  bootLines.forEach((line, i) => {
    setTimeout(() => printLine(line.text, line.type), i * 120);
  });
}

function executeCommand(cmd) {
  const input = document.getElementById('cmdInput');
  const command = cmd || (input ? input.value.trim() : '');
  if (!command) return;

  printLine(`> ${command}`, 'cmd');
  terminalHistory.unshift(command);
  historyIndex = -1;
  if (input) input.value = '';

  // Route command
  processCommand(command.toLowerCase());
}

function quickCmd(cmd) {
  const input = document.getElementById('cmdInput');
  if (input) input.value = cmd;
  executeCommand(cmd);
}

function processCommand(cmd) {
  const output = document.getElementById('terminalOutput');

  if (cmd === 'help') {
    ['Available commands:', '  launch <app>   – Launch application',
     '  open <app>     – Open application', '  browse <site>  – Open website',
     '  system status  – Show system stats', '  news briefing  – Latest news',
     '  check <app>    – App status', '  clear           – Clear terminal',
     '  tasks           – Show task list'].forEach(l => printLine(l, 'info'));
  } else if (cmd === 'clear') {
    if (output) output.innerHTML = '';
    printLine('Terminal cleared.', 'info');
  } else if (cmd === 'system status') {
    printLine('Running diagnostics...', 'info');
    setTimeout(() => {
      printLine('CPU: 34% — Optimal', 'res');
      printLine('RAM: 8.2 / 16 GB used', 'res');
      printLine('GPU: 1% idle', 'res');
      printLine('JARVIS AI Core: ACTIVE', 'res');
      printLine('All systems nominal.', 'res');
    }, 400);
  } else if (cmd.includes('obs') || cmd.includes('launch obs')) {
    printLine('Launching OBS Studio...', 'info');
    setTimeout(() => {
      printLine('OBS Studio is now running.', 'res');
      printLine('Scene: Gameplay — Stream ready.', 'res');
      toggleApp('obs', true);
      jarvisSpeak('OBS Studio launched. Your stream scene is active, sir.');
    }, 700);
  } else if (cmd.includes('steam')) {
    printLine('Opening Steam...', 'info');
    setTimeout(() => {
      printLine('Steam launched.', 'res');
      printLine('Recent: Counter-Strike 2 — 127 hrs', 'res');
      toggleApp('steam', true);
      jarvisSpeak('Steam is open. Counter-Strike 2 is recommended based on your playtime, sir.');
    }, 700);
  } else if (cmd.includes('youtube')) {
    printLine('Opening YouTube...', 'info');
    setTimeout(() => {
      printLine('YouTube loaded in browser.', 'res');
      toggleApp('youtube', true);
      jarvisSpeak('YouTube opened. Shall I search for something specific?');
    }, 600);
  } else if (cmd.includes('twitch')) {
    printLine('Checking Twitch...', 'info');
    setTimeout(() => {
      printLine('Twitch dashboard loaded.', 'res');
      printLine('Channel: DEXTER_AI — OFFLINE', 'warn');
      printLine('Tip: Go live to start streaming.', 'info');
      toggleApp('twitch', true);
      jarvisSpeak('Your Twitch channel is currently offline. Would you like me to start the stream?');
    }, 600);
  } else if (cmd.includes('news')) {
    printLine('Fetching news briefing...', 'info');
    setTimeout(() => {
      printLine('— Crimson Desert hits 27M hours opening week', 'res');
      printLine('— New AI model released: Claude 5 Opus', 'res');
      printLine('— Counter-Strike 2 major update drops', 'res');
      printLine('— Tech stocks rally on AI optimism', 'res');
      jarvisSpeak('Briefing complete. Crimson Desert is trending. Shall I open a full article?');
    }, 800);
  } else if (cmd.includes('tasks')) {
    const tasks = window.getTaskList ? window.getTaskList() : [];
    if (tasks.length === 0) {
      printLine('No tasks in queue.', 'info');
    } else {
      tasks.forEach((t, i) => printLine(`${i + 1}. [${t.done ? 'X' : ' '}] ${t.label}`, t.done ? 'info' : 'res'));
    }
  } else {
    printLine(`Processing: "${cmd}"...`, 'info');
    setTimeout(() => {
      jarvisSpeak(`I've received your command: ${cmd}. Processing now.`);
      printLine('Command acknowledged.', 'res');
    }, 500);
  }
}

// Keyboard navigation
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('cmdInput');
  if (!input) return;

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      executeCommand();
    } else if (e.key === 'ArrowUp') {
      historyIndex = Math.min(historyIndex + 1, terminalHistory.length - 1);
      input.value = terminalHistory[historyIndex] || '';
    } else if (e.key === 'ArrowDown') {
      historyIndex = Math.max(historyIndex - 1, -1);
      input.value = historyIndex >= 0 ? terminalHistory[historyIndex] : '';
    }
  });
});
