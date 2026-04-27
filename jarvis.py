"""
jarvis.py — The AI brain of JARVIS (powered by Google Gemini - FREE)
Get your free API key at: https://aistudio.google.com/apikey
"""

import os
import json
import google.generativeai as genai
from actions import JarvisActions
from voice import VoiceEngine

# ─── Setup ────────────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are JARVIS, an advanced AI assistant that controls a user's PC.
You respond concisely and helpfully. When you need to perform a PC action, respond with:

ACTION: <action_name> | PARAMS: <json_params>

Available actions:
- launch_app: {"app": "obs"|"steam"|"chrome"|"firefox"|"discord"|"spotify"|"vscode"}
- open_url: {"url": "https://..."}
- steam_game: {"game_id": "steam_id", "game_name": "Game Name"}
- youtube_search: {"query": "search term"}
- twitch_check: {"username": "your_username"}
- set_volume: {"level": 0-100}
- system_sleep: {}
- obs_start_stream: {}
- obs_stop_stream: {}
- obs_start_recording: {}
- news_search: {"topic": "topic"}
- type_text: {"text": "text to type"}
- screenshot: {}

Always confirm what action you're taking in plain English AFTER the action line.
Be brief. Sound like a real assistant, not a robot."""


class Jarvis:
    def __init__(self):
        self.actions = JarvisActions()
        self.voice = VoiceEngine()
        # gemini-1.5-flash is FREE with generous limits
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        self.chat_session = self.model.start_chat(history=[])

    def chat(self, user_message: str) -> dict:
        response = self.chat_session.send_message(user_message)
        reply = response.text
        action_result = self._parse_and_execute(reply)
        human_reply = self._extract_human_reply(reply)
        return {"reply": human_reply, "action": action_result, "raw": reply}

    def _parse_and_execute(self, reply: str):
        if "ACTION:" not in reply:
            return None
        try:
            action_line = [l for l in reply.split('\n') if l.startswith("ACTION:")][0]
            parts = action_line.split("|")
            action_name = parts[0].replace("ACTION:", "").strip()
            params = {}
            if len(parts) > 1 and "PARAMS:" in parts[1]:
                params = json.loads(parts[1].replace("PARAMS:", "").strip())
            return self.actions.execute(action_name, params)
        except Exception as e:
            return {"error": str(e)}

    def _extract_human_reply(self, reply: str) -> str:
        lines = [l for l in reply.split('\n') if not l.startswith("ACTION:")]
        return '\n'.join(lines).strip()

    def speak(self, text: str):
        self.voice.speak(text)

    def listen(self) -> str:
        return self.voice.listen()

    def clear_history(self):
        self.chat_session = self.model.start_chat(history=[])


if __name__ == "__main__":
    jarvis = Jarvis()
    print("JARVIS online (Google Gemini - FREE)")
    print("Get key: https://aistudio.google.com/apikey")
    print("-" * 50)
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ("quit", "exit"):
                break
            result = jarvis.chat(user_input)
            print(f"\nJARVIS: {result['reply']}")
        except KeyboardInterrupt:
            break
