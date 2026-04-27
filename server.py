"""
server.py — Flask API server for JARVIS (Google Gemini edition)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading
import os
from jarvis import Jarvis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jarvis-secret'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

jarvis = Jarvis()
is_listening = False


@app.route('/health')
def health():
    return jsonify({"status": "online", "model": "gemini-1.5-flash", "message": "JARVIS online."})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').strip()
    if not message:
        return jsonify({"error": "No message"}), 400
    result = jarvis.chat(message)
    threading.Thread(target=jarvis.speak, args=(result['reply'],), daemon=True).start()
    return jsonify(result)


@app.route('/voice/start', methods=['POST'])
def voice_start():
    global is_listening
    if is_listening:
        return jsonify({"error": "Already listening"}), 400
    is_listening = True

    def listen_and_respond():
        global is_listening
        text = jarvis.listen()
        is_listening = False
        if text:
            socketio.emit('voice_heard', {'text': text})
            result = jarvis.chat(text)
            socketio.emit('jarvis_reply', result)
            threading.Thread(target=jarvis.speak, args=(result['reply'],), daemon=True).start()
        else:
            socketio.emit('voice_heard', {'text': '', 'error': 'Nothing heard'})

    threading.Thread(target=listen_and_respond, daemon=True).start()
    return jsonify({"status": "listening"})


@app.route('/voice/stop', methods=['POST'])
def voice_stop():
    global is_listening
    is_listening = False
    return jsonify({"status": "stopped"})


@app.route('/clear', methods=['POST'])
def clear():
    jarvis.clear_history()
    return jsonify({"status": "cleared"})


@socketio.on('connect')
def on_connect():
    emit('connected', {'message': 'JARVIS backend connected (Gemini)'})


@socketio.on('chat_message')
def on_chat(data):
    result = jarvis.chat(data.get('message', ''))
    emit('jarvis_reply', result)
    threading.Thread(target=jarvis.speak, args=(result['reply'],), daemon=True).start()


if __name__ == '__main__':
    port = int(os.environ.get('JARVIS_PORT', 5000))
    print(f"JARVIS Backend (Gemini) starting on http://localhost:{port}")
    print("Make sure GEMINI_API_KEY is set!")
    jarvis.speak("JARVIS online. Gemini systems operational.", blocking=False)
    socketio.run(app, host='localhost', port=port, debug=False)
