const { app, BrowserWindow, ipcMain, globalShortcut, Tray, Menu } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let overlayWindow;
let tray;
let backendProcess;

// ─── Start Python Backend ────────────────────────────────────────────────────
function startBackend() {
  backendProcess = spawn('python', [path.join(__dirname, 'backend', 'server.py')], {
    env: { ...process.env },
    stdio: 'pipe'
  });

  backendProcess.stdout.on('data', (data) => {
    console.log(`[JARVIS Backend]: ${data}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.error(`[JARVIS Backend Error]: ${data}`);
  });

  backendProcess.on('close', (code) => {
    console.log(`Backend exited with code ${code}`);
  });
}

// ─── Main HUD Window ─────────────────────────────────────────────────────────
function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 420,
    height: 700,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: false,
    skipTaskbar: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
    icon: path.join(__dirname, 'frontend/public/icon.png'),
  });

  // In dev: load React dev server; in prod: load built files
  const isDev = process.env.NODE_ENV === 'development';
  if (isDev) {
    mainWindow.loadURL('http://localhost:3000');
    mainWindow.webContents.openDevTools({ mode: 'detach' });
  } else {
    mainWindow.loadFile(path.join(__dirname, 'frontend/build/index.html'));
  }

  mainWindow.setPosition(20, 100);
}

// ─── System Tray ─────────────────────────────────────────────────────────────
function createTray() {
  tray = new Tray(path.join(__dirname, 'frontend/public/icon.png'));
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Show JARVIS', click: () => mainWindow.show() },
    { label: 'Hide JARVIS', click: () => mainWindow.hide() },
    { type: 'separator' },
    { label: 'Quit', click: () => app.quit() }
  ]);
  tray.setToolTip('JARVIS - AI Assistant');
  tray.setContextMenu(contextMenu);
  tray.on('click', () => {
    mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
  });
}

// ─── Global Shortcuts ─────────────────────────────────────────────────────────
function registerShortcuts() {
  // Ctrl+Shift+J → Toggle JARVIS overlay
  globalShortcut.register('CommandOrControl+Shift+J', () => {
    if (mainWindow.isVisible()) {
      mainWindow.hide();
    } else {
      mainWindow.show();
      mainWindow.focus();
    }
  });

  // Ctrl+Shift+V → Push-to-talk voice command
  globalShortcut.register('CommandOrControl+Shift+V', () => {
    mainWindow.webContents.send('trigger-voice');
  });
}

// ─── IPC Handlers ─────────────────────────────────────────────────────────────
ipcMain.on('minimize-window', () => mainWindow.minimize());
ipcMain.on('close-window', () => mainWindow.hide());
ipcMain.on('drag-window', (event, { x, y }) => mainWindow.setPosition(x, y));

// ─── App Lifecycle ────────────────────────────────────────────────────────────
app.whenReady().then(() => {
  startBackend();

  // Give backend a moment to start
  setTimeout(() => {
    createMainWindow();
    createTray();
    registerShortcuts();
  }, 2000);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createMainWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
  if (backendProcess) backendProcess.kill();
});
