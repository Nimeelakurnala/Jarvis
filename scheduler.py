"""
scheduler.py — Automated Routines for JARVIS
Runs scheduled tasks like morning briefing, news updates, stream reminders, etc.
"""

import schedule
import time
import json
import threading
import os


def load_routines() -> list:
    """Load routines from config file."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'routines.json')
    try:
        with open(config_path) as f:
            return json.load(f)
    except FileNotFoundError:
        return []


class JarvisScheduler:
    """Manages timed routines and scheduled Jarvis commands."""

    def __init__(self, jarvis_instance):
        self.jarvis = jarvis_instance
        self._running = False
        self._thread = None

    def setup_default_routines(self):
        """Register built-in scheduled tasks."""

        # ── Good Morning Briefing (8:00 AM daily) ─────────────────────────────
        schedule.every().day.at("08:00").do(self.morning_briefing)

        # ── Gaming News Check (6:00 PM) ────────────────────────────────────────
        schedule.every().day.at("18:00").do(self.gaming_news_check)

        # ── Stream Reminder (custom — set in routines.json) ────────────────────
        routines = load_routines()
        for routine in routines:
            self._register_routine(routine)

        print("[JARVIS Scheduler] Routines loaded.")

    def _register_routine(self, routine: dict):
        """Dynamically register a routine from config."""
        time_str = routine.get("time")
        command = routine.get("command")
        days = routine.get("days", "daily")

        if not time_str or not command:
            return

        def run_task():
            result = self.jarvis.chat(command)
            self.jarvis.speak(result['reply'])

        if days == "daily":
            schedule.every().day.at(time_str).do(run_task)
        elif days == "weekday":
            for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
                getattr(schedule.every(), day).at(time_str).do(run_task)
        elif days == "weekend":
            schedule.every().saturday.at(time_str).do(run_task)
            schedule.every().sunday.at(time_str).do(run_task)

    def morning_briefing(self):
        """Morning routine — brief the user on their day."""
        print("[JARVIS] Running morning briefing...")
        briefing = self.jarvis.chat(
            "Give me a brief good morning greeting and open today's gaming news."
        )
        self.jarvis.speak(briefing['reply'])

    def gaming_news_check(self):
        """Evening gaming news check."""
        print("[JARVIS] Evening gaming news check...")
        result = self.jarvis.chat("What's trending in gaming today? Open the news.")
        self.jarvis.speak(result['reply'])

    def start(self):
        """Start the scheduler in a background thread."""
        self.setup_default_routines()
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        print("[JARVIS Scheduler] Running.")

    def stop(self):
        """Stop the scheduler."""
        self._running = False
        schedule.clear()

    def _run_loop(self):
        """Scheduler tick loop."""
        while self._running:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
