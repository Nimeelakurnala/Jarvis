"""
voice.py — Voice Recognition & Text-to-Speech for JARVIS
Uses SpeechRecognition + pyttsx3 for offline TTS.
"""

import speech_recognition as sr
import pyttsx3
import threading
import time


class VoiceEngine:
    """Handles microphone input and speech output."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self._init_tts()
        self._calibrate_mic()

    def _init_tts(self):
        """Initialize text-to-speech engine."""
        self.tts = pyttsx3.init()
        voices = self.tts.getProperty('voices')

        # Prefer a deeper, cleaner voice (like JARVIS from Iron Man)
        for voice in voices:
            if 'david' in voice.name.lower() or 'male' in voice.name.lower():
                self.tts.setProperty('voice', voice.id)
                break

        self.tts.setProperty('rate', 185)    # Speed (words per minute)
        self.tts.setProperty('volume', 0.95) # Volume (0.0 to 1.0)

    def _calibrate_mic(self):
        """Calibrate microphone for ambient noise."""
        print("[JARVIS Voice] Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[JARVIS Voice] Microphone ready.")

    def listen(self, timeout: int = 8, phrase_limit: int = 10) -> str:
        """
        Listen for a voice command and return transcribed text.
        Returns empty string if nothing is heard.
        """
        print("[JARVIS] Listening...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )

            text = self.recognizer.recognize_google(audio)
            print(f"[JARVIS] Heard: {text}")
            return text.lower()

        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"[JARVIS Voice Error] {e}")
            return ""

    def speak(self, text: str, blocking: bool = False):
        """
        Speak text aloud using TTS.
        Non-blocking by default (runs in a thread).
        """
        # Strip markdown/special chars for cleaner speech
        clean = text.replace("*", "").replace("#", "").replace("`", "")

        if blocking:
            self.tts.say(clean)
            self.tts.runAndWait()
        else:
            thread = threading.Thread(target=self._speak_thread, args=(clean,), daemon=True)
            thread.start()

    def _speak_thread(self, text: str):
        self.tts.say(text)
        self.tts.runAndWait()

    def wait_for_wake_word(self, wake_word: str = "jarvis") -> bool:
        """
        Continuously listen until the wake word is detected.
        Returns True when wake word is heard.
        """
        print(f"[JARVIS] Waiting for wake word: '{wake_word}'")
        while True:
            heard = self.listen(timeout=5)
            if wake_word in heard:
                self.speak("Yes, I'm here.")
                return True
            time.sleep(0.1)
