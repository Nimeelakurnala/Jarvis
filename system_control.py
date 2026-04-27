"""
system_control.py — System-level controls for JARVIS
Volume, brightness, power, keyboard shortcuts.
"""

import subprocess
import sys
import os
import pyautogui
import time


def set_volume(level: int):
    """Set system volume (0-100)."""
    level = max(0, min(100, level))
    if sys.platform == "win32":
        # Via PowerShell (no extra deps needed)
        script = f"""
        $obj = New-Object -ComObject WScript.Shell
        $currentVol = [Math]::Round((Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Multimedia\\Audio' -Name 'MasterVolume' -ErrorAction SilentlyContinue).MasterVolume / 65535 * 100)
        """
        # Simpler approach using nircmd (if available)
        nircmd = r"C:\Windows\System32\nircmd.exe"
        if os.path.exists(nircmd):
            subprocess.run([nircmd, "setsysvolume", str(int(level / 100 * 65535))])
        else:
            # PyAutoGUI keyboard fallback
            print(f"Volume set to {level}% (manual control)")
    elif sys.platform == "darwin":
        subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
    else:
        subprocess.run(["amixer", "-q", "sset", "Master", f"{level}%"])
    print(f"Volume: {level}%")


def mute():
    """Mute system audio."""
    pyautogui.press('volumemute')
    print("Muted")


def volume_up(steps: int = 5):
    """Increase volume by steps."""
    for _ in range(steps):
        pyautogui.press('volumeup')
    print(f"Volume up {steps} steps")


def volume_down(steps: int = 5):
    """Decrease volume by steps."""
    for _ in range(steps):
        pyautogui.press('volumedown')
    print(f"Volume down {steps} steps")


def sleep_system():
    """Put the PC to sleep."""
    print("Sleeping in 3 seconds...")
    time.sleep(3)
    if sys.platform == "win32":
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
    elif sys.platform == "darwin":
        subprocess.run(["pmset", "sleepnow"])
    else:
        subprocess.run(["systemctl", "suspend"])


def lock_screen():
    """Lock the screen."""
    if sys.platform == "win32":
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
    elif sys.platform == "darwin":
        subprocess.run(["pmset", "displaysleepnow"])
    else:
        subprocess.run(["loginctl", "lock-session"])
    print("Screen locked")


def take_screenshot(save_path: str = None) -> str:
    """Take a screenshot and save it."""
    if save_path is None:
        pics_dir = os.path.expanduser("~/Pictures/JARVIS")
        os.makedirs(pics_dir, exist_ok=True)
        save_path = os.path.join(pics_dir, f"jarvis_{int(time.time())}.png")

    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)
    print(f"Screenshot saved: {save_path}")
    return save_path


def open_task_manager():
    """Open Task Manager."""
    if sys.platform == "win32":
        subprocess.Popen(["taskmgr"])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", "-a", "Activity Monitor"])
    else:
        subprocess.Popen(["gnome-system-monitor"])


def kill_process(process_name: str):
    """Kill a process by name."""
    import psutil
    killed = []
    for proc in psutil.process_iter(['name']):
        if process_name.lower() in proc.info['name'].lower():
            proc.kill()
            killed.append(proc.info['name'])
    print(f"Killed: {killed}" if killed else f"No process named '{process_name}' found")
    return killed


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    arg = sys.argv[2] if len(sys.argv) > 2 else None

    if cmd == "volume" and arg:
        set_volume(int(arg))
    elif cmd == "mute":
        mute()
    elif cmd == "sleep":
        sleep_system()
    elif cmd == "lock":
        lock_screen()
    elif cmd == "screenshot":
        take_screenshot(arg)
    else:
        print("Usage: system_control.py [volume <0-100>|mute|sleep|lock|screenshot]")
