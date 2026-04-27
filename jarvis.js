// ===== JARVIS AI RESPONSE ENGINE =====
// Connects to Anthropic API to generate Jarvis-style responses

const JARVIS_SYSTEM = `You are JARVIS (Just A Rather Very Intelligent System), 
an advanced AI life manager inspired by Iron Man's JARVIS. 
You control apps, manage tasks, browse the web, and assist the user with everything.
You are calm, precise, witty, and always address the user as "sir."
Keep responses concise (1-3 sentences max). Always stay in character.
Reference apps like OBS, Steam, Twitch, YouTube, Discord when relevant.`;

async function callJarvisAI(userMessage) {
  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 150,
        system: JARVIS_SYSTEM,
        messages: [{ role: 'user', content: userMessage }]
      })
    });

    const data = await response.json();
    if (data.content && data.content[0] && data.content[0].text) {
      return data.content[0].text.trim();
    }
    return null;
  } catch (err) {
    console.error('Jarvis API error:', err);
    return null;
  }
}

// Fallback local responses when API unavailable
const localResponses = {
  default: [
    "Understood, sir. Processing your request now.",
    "Right away, sir. Consider it done.",
    "Of course, sir. I'm on it.",
    "Acknowledged, sir. Executing command.",
    "Certainly, sir. I'll handle that immediately.",
  ],
  greeting: [
    "Good to see you, sir. All systems are operational.",
    "Welcome back, sir. Shall I run the usual startup sequence?",
    "At your service, sir. How may I assist you today?",
  ],
  obs: ["OBS Studio is ready, sir. Your stream scene is loaded and audio levels are optimal."],
  steam: ["Steam is open, sir. Counter-Strike 2 has a new update available."],
  twitch: ["Your Twitch channel is set up, sir. You have 3 new followers since yesterday."],
  youtube: ["YouTube is open, sir. Shall I search for something specific?"],
  news: ["News briefing complete, sir. Crimson Desert is trending with 27 million hours in its opening week."],
};

function getLocalResponse(context) {
  const ctx = context.toLowerCase();
  for (const key of Object.keys(localResponses)) {
    if (key !== 'default' && ctx.includes(key)) {
      const arr = localResponses[key];
      return arr[Math.floor(Math.random() * arr.length)];
    }
  }
  const arr = localResponses.default;
  return arr[Math.floor(Math.random() * arr.length)];
}

async function jarvisSpeak(message, context = '') {
  const responseBox = document.getElementById('responseBox');
  if (!responseBox) return;

  // Show thinking state
  setCoreStatus('THINKING', 'busy');
  responseBox.innerHTML = `
    <div class="response-text">
      <div class="r-prefix">JARVIS RESPONSE</div>
      <span style="color:var(--text-dim)">Processing<span class="typing-cursor"></span></span>
    </div>
  `;

  // Log incoming message
  addLog('action', 'AI', `Query: "${message.substring(0, 40)}${message.length > 40 ? '…' : ''}"`);

  // Try to get AI response
  let reply = await callJarvisAI(message);
  if (!reply) reply = getLocalResponse(context || message);

  // Animate response
  setCoreStatus('ACTIVE', 'active');
  responseBox.innerHTML = `
    <div class="response-text">
      <div class="r-prefix">▶ JARVIS SAYS</div>
      <div id="jarvisTyped"></div>
    </div>
  `;

  const typed = document.getElementById('jarvisTyped');
  let i = 0;
  const interval = setInterval(() => {
    if (i < reply.length) {
      typed.textContent += reply[i];
      i++;
    } else {
      clearInterval(interval);
      setTimeout(() => setCoreStatus('STANDBY', ''), 3000);
      addLog('ok', 'AI', `Response delivered`);
    }
  }, 20);
}

// Export globally
window.jarvisSpeak = jarvisSpeak;
