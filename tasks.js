// ===== TASK MANAGER COMPONENT =====
const tasks = [
  { id: 1, label: 'Start OBS & go live on Twitch', priority: 'high', done: false },
  { id: 2, label: 'Check Counter-Strike 2 update', priority: 'med', done: false },
  { id: 3, label: 'Watch Crimson Desert launch video', priority: 'low', done: false },
  { id: 4, label: 'Review news briefing', priority: 'med', done: false },
  { id: 5, label: 'Organize stream schedule', priority: 'high', done: false },
];
let taskIdCounter = 6;

function renderTasks() {
  const list = document.getElementById('taskList');
  if (!list) return;
  list.innerHTML = '';
  tasks.forEach(task => {
    const item = document.createElement('div');
    item.className = `task-item${task.done ? ' done' : ''}`;
    item.id = `task-${task.id}`;
    item.innerHTML = `
      <div class="task-check" onclick="toggleTask(${task.id})">${task.done ? '✓' : ''}</div>
      <div class="task-label">${task.label}</div>
      <div class="task-priority ${task.priority}">${task.priority.toUpperCase()}</div>
      <div class="task-del" onclick="deleteTask(${task.id})">✕</div>
    `;
    list.appendChild(item);
  });
}

function addTask() {
  const input = document.getElementById('taskInput');
  if (!input || !input.value.trim()) return;
  const label = input.value.trim();
  tasks.push({ id: taskIdCounter++, label, priority: 'med', done: false });
  input.value = '';
  renderTasks();
  addLog('action', 'TASK', `New task added: "${label}"`);
  jarvisSpeak(`Task added: ${label}`);
}

function toggleTask(id) {
  const task = tasks.find(t => t.id === id);
  if (!task) return;
  task.done = !task.done;
  renderTasks();
  if (task.done) {
    addLog('ok', 'TASK', `Completed: "${task.label}"`);
    jarvisSpeak(`Task completed: ${task.label}`);
  }
}

function deleteTask(id) {
  const idx = tasks.findIndex(t => t.id === id);
  if (idx >= 0) {
    addLog('warn', 'TASK', `Removed: "${tasks[idx].label}"`);
    tasks.splice(idx, 1);
    renderTasks();
  }
}

// Expose for terminal
window.getTaskList = () => tasks;

// Enter key for task input
document.addEventListener('DOMContentLoaded', () => {
  const ti = document.getElementById('taskInput');
  if (ti) ti.addEventListener('keydown', e => { if (e.key === 'Enter') addTask(); });
});
