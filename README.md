# 🤖 JARVIS — Your AI Life Manager (Google Gemini Edition — FREE)

> *"POV: you built Jarvis to run your life"*

Powered by **Google Gemini 1.5 Flash** — completely FREE, no credit card needed.

---

## 🔑 Step 1: Get Your FREE Gemini API Key (2 minutes)

1. Go to 👉 **https://aistudio.google.com/apikey**
2. Sign in with your **Google account**
3. Click **"Create API Key"**
4. Copy the key (looks like: `AIzaSy...`)

That's it — it's 100% FREE with generous daily limits!

---

## 📁 Project Structure

```
jarvis-ai/
├── backend/
│   ├── jarvis.py          # AI brain (Google Gemini)
│   ├── actions.py         # PC control (OBS, Steam, browser...)
│   ├── voice.py           # Voice recognition & TTS
│   ├── scheduler.py       # Daily routines
│   └── server.py          # Flask API server
├── frontend/
│   └── public/index.html  # Holographic HUD overlay
├── scripts/
│   ├── launch_obs.py      # OBS control
│   └── system_control.py  # Volume, sleep, lock
├── config/
│   ├── settings.json      # Your preferences
│   └── routines.json      # Scheduled routines
├── main.js                # Electron desktop app
├── package.json
└── requirements.txt
```

---

## 🚀 Setup & Run

### 1. Install Python packages
```bash
pip install -r requirements.txt
```

### 2. Install Node packages
```bash
npm install
```

### 3. Set your FREE Gemini API key

**Windows:**
```bash
set GEMINI_API_KEY=AIzaSy_YOUR_KEY_HERE
```

**Mac/Linux:**
```bash
export GEMINI_API_KEY=AIzaSy_YOUR_KEY_HERE
```

### 4. Run JARVIS!
```bash
# Terminal 1 — Start the AI backend
python backend/server.py

# Terminal 2 — Start the HUD overlay
npm start
```

---

## 🗣️ Example Commands

- *"Jarvis, open OBS and start my stream"*
- *"Launch Counter-Strike 2 on Steam"*
- *"What's the latest gaming news?"*
- *"Search YouTube for Crimson Desert trailer"*
- *"Check my Twitch channel"*
- *"Set volume to 50%"*
- *"Take a screenshot"*

---

## 💡 Gemini Free Tier Limits

| Model | Free Requests/Day |
|---|---|
| gemini-1.5-flash | 1,500 / day |
| gemini-1.5-pro | 50 / day |

**gemini-1.5-flash** is used by default — 1,500 requests/day is more than enough for daily JARVIS use!

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+Shift+J` | Toggle JARVIS HUD |
| `Ctrl+Shift+V` | Push-to-talk voice |

