"""
launch_obs.py — OBS Studio launcher and scene switcher for JARVIS
"""

import subprocess
import time
import os
import sys

try:
    import obsws_python as obs
    OBS_AVAILABLE = True
except ImportError:
    OBS_AVAILABLE = False

OBS_PATH = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = "your_password"  # Set in config/settings.json


def launch_obs(minimized: bool = False):
    """Launch OBS Studio."""
    if not os.path.exists(OBS_PATH):
        print(f"OBS not found at {OBS_PATH}")
        return False

    args = [OBS_PATH]
    if minimized:
        args.append("--minimize-to-tray")

    subprocess.Popen(args)
    print("OBS launched. Waiting for startup...")
    time.sleep(4)
    return True


def start_stream():
    """Start streaming via OBS WebSocket."""
    if not OBS_AVAILABLE:
        print("obs-websocket-py not installed. Run: pip install obs-websocket-py")
        return

    try:
        cl = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)
        cl.start_stream()
        print("✅ Stream started!")
    except Exception as e:
        print(f"OBS WebSocket error: {e}")


def stop_stream():
    """Stop streaming via OBS WebSocket."""
    if not OBS_AVAILABLE:
        return

    try:
        cl = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)
        cl.stop_stream()
        print("⏹️ Stream stopped.")
    except Exception as e:
        print(f"OBS WebSocket error: {e}")


def switch_scene(scene_name: str):
    """Switch OBS to a specific scene."""
    if not OBS_AVAILABLE:
        return

    try:
        cl = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)
        cl.set_current_program_scene(scene_name)
        print(f"Switched to scene: {scene_name}")
    except Exception as e:
        print(f"Scene switch error: {e}")


def get_stream_status() -> dict:
    """Get current stream status."""
    if not OBS_AVAILABLE:
        return {"error": "OBS WebSocket not available"}

    try:
        cl = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)
        status = cl.get_stream_status()
        return {
            "active": status.output_active,
            "timecode": status.output_timecode,
            "bytes": status.output_bytes
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "launch"

    commands = {
        "launch": launch_obs,
        "start_stream": start_stream,
        "stop_stream": stop_stream,
        "status": lambda: print(get_stream_status()),
    }

    action = commands.get(cmd)
    if action:
        action()
    else:
        print(f"Unknown command: {cmd}")
        print(f"Available: {', '.join(commands.keys())}")
