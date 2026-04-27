"""
actions.py — PC Control Actions for JARVIS
Handles launching apps, browser control, OBS, system commands, etc.
"""

import subprocess
import webbrowser
import os
import sys
import time
import requests
import pyautogui
import psutil

# Optional: OBS WebSocket (install obs-websocket-py)
try:
    import obsws_python as obs
    OBS_AVAILABLE = True
except ImportError:
    OBS_AVAILABLE = False

# Optional: Windows-only volume control
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    VOLUME_CONTROL = True
except ImportError:
    VOLUME_CONTROL = False


# ─── App Paths (Windows defaults — customize for your setup) ──────────────────
APP_PATHS = {
    "obs": r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "discord": os.path.expanduser(r"~\AppData\Local\Discord\Update.exe"),
    "spotify": os.path.expanduser(r"~\AppData\Roaming\Spotify\Spotify.exe"),
    "vscode": r"C:\Program Files\Microsoft VS Code\Code.exe",
    "notepad": r"C:\Windows\notepad.exe",
    "calculator": r"C:\Windows\System32\calc.exe",
}

# OBS WebSocket config (set in config/settings.json)
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = "your_obs_password"


class JarvisActions:
    """All PC actions JARVIS can perform."""

    def execute(self, action_name: str, params: dict) -> dict:
        """Route action name to the correct handler."""
        handlers = {
            "launch_app": self.launch_app,
            "open_url": self.open_url,
            "steam_game": self.launch_steam_game,
            "youtube_search": self.youtube_search,
            "twitch_check": self.twitch_check,
            "set_volume": self.set_volume,
            "system_sleep": self.system_sleep,
            "obs_start_stream": self.obs_start_stream,
            "obs_stop_stream": self.obs_stop_stream,
            "obs_start_recording": self.obs_start_recording,
            "news_search": self.news_search,
            "type_text": self.type_text,
            "screenshot": self.take_screenshot,
        }

        handler = handlers.get(action_name)
        if not handler:
            return {"success": False, "error": f"Unknown action: {action_name}"}

        try:
            result = handler(**params)
            return {"success": True, "action": action_name, "result": result}
        except Exception as e:
            return {"success": False, "action": action_name, "error": str(e)}

    # ─── App Launcher ─────────────────────────────────────────────────────────
    def launch_app(self, app: str) -> str:
        app = app.lower()
        path = APP_PATHS.get(app)

        if path and os.path.exists(path):
            subprocess.Popen([path])
            return f"Launched {app}"

        # Fallback: try to open by name
        try:
            if sys.platform == "win32":
                subprocess.Popen(["start", app], shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-a", app])
            else:
                subprocess.Popen([app])
            return f"Launched {app}"
        except Exception as e:
            return f"Could not launch {app}: {e}"

    # ─── Browser / URL ────────────────────────────────────────────────────────
    def open_url(self, url: str) -> str:
        webbrowser.open(url)
        return f"Opened {url}"

    # ─── Steam Game ───────────────────────────────────────────────────────────
    def launch_steam_game(self, game_id: str = "", game_name: str = "") -> str:
        if game_id:
            subprocess.Popen(["start", f"steam://rungameid/{game_id}"], shell=True)
            return f"Launching {game_name} via Steam"
        return "No game ID provided"

    # ─── YouTube ──────────────────────────────────────────────────────────────
    def youtube_search(self, query: str) -> str:
        import urllib.parse
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        webbrowser.open(search_url)
        return f"Searching YouTube for: {query}"

    # ─── Twitch Status ────────────────────────────────────────────────────────
    def twitch_check(self, username: str) -> str:
        url = f"https://www.twitch.tv/{username}"
        webbrowser.open(url)
        return f"Opening Twitch channel: {username}"

    # ─── Volume Control ───────────────────────────────────────────────────────
    def set_volume(self, level: int) -> str:
        level = max(0, min(100, int(level)))

        if VOLUME_CONTROL:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            # Convert 0-100 to scalar 0.0-1.0
            volume.SetMasterVolumeLevelScalar(level / 100, None)
        elif sys.platform == "win32":
            # Fallback via PowerShell
            ps_cmd = f"(Get-AudioDevice -Playback).Volume = {level}"
            subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
        elif sys.platform == "darwin":
            subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
        else:
            subprocess.run(["amixer", "-q", "sset", "Master", f"{level}%"])

        return f"Volume set to {level}%"

    # ─── System Sleep ─────────────────────────────────────────────────────────
    def system_sleep(self) -> str:
        if sys.platform == "win32":
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
        elif sys.platform == "darwin":
            subprocess.run(["pmset", "sleepnow"])
        else:
            subprocess.run(["systemctl", "suspend"])
        return "System sleeping"

    # ─── OBS Control ──────────────────────────────────────────────────────────
    def _obs_connect(self):
        if not OBS_AVAILABLE:
            raise RuntimeError("obs-websocket-py not installed")
        return obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD)

    def obs_start_stream(self) -> str:
        cl = self._obs_connect()
        cl.start_stream()
        return "OBS stream started"

    def obs_stop_stream(self) -> str:
        cl = self._obs_connect()
        cl.stop_stream()
        return "OBS stream stopped"

    def obs_start_recording(self) -> str:
        cl = self._obs_connect()
        cl.start_record()
        return "OBS recording started"

    # ─── News Search ──────────────────────────────────────────────────────────
    def news_search(self, topic: str) -> str:
        import urllib.parse
        url = f"https://news.google.com/search?q={urllib.parse.quote(topic)}"
        webbrowser.open(url)
        return f"Opened news for: {topic}"

    # ─── Type Text ────────────────────────────────────────────────────────────
    def type_text(self, text: str) -> str:
        time.sleep(0.5)
        pyautogui.typewrite(text, interval=0.05)
        return f"Typed: {text}"

    # ─── Screenshot ───────────────────────────────────────────────────────────
    def take_screenshot(self) -> str:
        screenshot_dir = os.path.expanduser("~/Pictures/JARVIS")
        os.makedirs(screenshot_dir, exist_ok=True)
        filepath = os.path.join(screenshot_dir, f"jarvis_{int(time.time())}.png")
        pyautogui.screenshot(filepath)
        return f"Screenshot saved: {filepath}"
