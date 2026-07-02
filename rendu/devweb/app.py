import streamlit as st
import requests
from pathlib import Path

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "techcorp-financial"
ASSETS = Path(__file__).parent / "assets"

st.set_page_config(
    page_title="TechCorp | Assistant Financier",
    page_icon=str(ASSETS / "icon.png"),
    layout="centered",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stApp, .stMarkdown, p, span, label, div,
    [data-testid="stChatMessage"] p, .stChatInput textarea {
        font-family: 'Montserrat', sans-serif !important;
    }

    .stApp { background: #0a0e27; }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { padding-top: 1.5rem; max-width: 760px; }

    .tc-badge {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 6px 14px; border-radius: 999px; font-size: 13px; font-weight: 600;
        margin-bottom: 1.5rem;
    }
    .tc-badge.online { background: rgba(46, 213, 115, 0.12); color: #2ed573; border: 1px solid rgba(46, 213, 115, 0.35); }
    .tc-badge.offline { background: rgba(255, 71, 87, 0.12); color: #ff4757; border: 1px solid rgba(255, 71, 87, 0.35); }
    .tc-dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; display: inline-block; }

    [data-testid="stChatMessage"] {
        background: #131736; border: 1px solid #22274d; border-radius: 14px;
        padding: 4px 6px;
    }
    .stChatInput textarea, [data-testid="stChatInput"] textarea {
        background: #131736 !important; color: #ffffff !important; border-color: #22274d !important;
    }
    [data-testid="stChatInput"] { background: #0a0e27; border-top: 1px solid #22274d; }

    h1, h2, h3, p, span, label, .stMarkdown { color: #e8eaf6; }
    .tc-footer { text-align: center; color: #565b8f; font-size: 12px; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

ANIMATED_ICON = '''
<style>
@keyframes float { 0%, 100% { transform: translateY(0px) rotate(0deg); } 30% { transform: translateY(-10px) rotate(0.5deg); } 70% { transform: translateY(-6px) rotate(-0.5deg); } }
@keyframes roof-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
@keyframes look { 0%, 15% { transform: translateX(0) scaleY(1); } 25%, 40% { transform: translateX(4px) scaleY(1); } 50%, 65% { transform: translateX(-4px) scaleY(1); } 75%, 88% { transform: translateX(0) scaleY(1); } 92% { transform: translateX(0) scaleY(0.06); } 96%, 100% { transform: translateX(0) scaleY(1); } }
@keyframes talk { 0%, 100% { transform: scaleY(1); } 25% { transform: scaleY(1.5); } 50% { transform: scaleY(0.7); } 75% { transform: scaleY(1.8); } }
@keyframes pulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.02); opacity: 0.92; } }
@keyframes ring-glow { 0%, 100% { opacity: 0.18; } 50% { opacity: 0.35; } }
.bot-icon { display:inline-block; filter: drop-shadow(0 16px 40px rgba(79, 70, 229, 0.28)); }
#g-body { animation: float 3.4s ease-in-out infinite; transform-origin: 200px 230px; }
#g-roof { animation: roof-float 2.8s ease-in-out infinite; transform-origin: 200px 120px; }
#g-bubble { animation: pulse 3.4s ease-in-out infinite; transform-origin: 200px 210px; }
#ring { animation: ring-glow 3.4s ease-in-out infinite; }
#eye-l { transform-origin: 165px 235px; animation: look 6s ease-in-out infinite; }
#eye-r { transform-origin: 235px 235px; animation: look 6s ease-in-out infinite; }
#mouth-path { transform-origin: 200px 262px; animation: talk 0.6s ease-in-out infinite; }
</style>
<svg class="bot-icon" width="200" height="220" viewBox="0 0 400 440" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Assistant TechCorp anime">
  <defs>
    <linearGradient id="gBlue" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2563EB"/><stop offset="100%" stop-color="#06B6D4"/></linearGradient>
    <linearGradient id="gPurple" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#4F46E5"/><stop offset="100%" stop-color="#9333EA"/></linearGradient>
    <linearGradient id="gFace" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#1e2a6e"/><stop offset="100%" stop-color="#060b24"/></linearGradient>
    <linearGradient id="gBubble" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#f0f4ff"/></linearGradient>
    <filter id="fShadow" x="-15%" y="-15%" width="130%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#4F46E5" flood-opacity="0.22"/></filter>
    <filter id="fGlow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <g id="g-bubble">
    <circle id="ring" cx="200" cy="205" r="192" fill="none" stroke="#c7d2fe" stroke-width="3"/>
    <circle cx="200" cy="205" r="178" fill="url(#gBubble)" stroke="#e0e7ff" stroke-width="1.5"/>
    <path d="M 148 375 Q 132 408 110 425 Q 140 412 168 388 Z" fill="url(#gBubble)"/>
  </g>
  <g id="g-body" filter="url(#fShadow)">
    <g id="g-roof"><path d="M 88 178 L 200 88 L 312 178" fill="none" stroke="url(#gBlue)" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/></g>
    <rect x="90" y="196" width="52" height="18" rx="9" fill="url(#gBlue)"/>
    <rect x="258" y="196" width="52" height="18" rx="9" fill="url(#gBlue)"/>
    <path d="M 112 214 L 76 272 L 128 296 L 158 256 Z" fill="url(#gPurple)"/>
    <path d="M 288 214 L 324 272 L 272 296 L 242 256 Z" fill="url(#gPurple)"/>
    <rect x="188" y="296" width="24" height="36" rx="12" fill="url(#gPurple)"/>
    <rect x="112" y="196" width="176" height="96" rx="26" fill="url(#gBlue)"/>
    <rect x="126" y="206" width="148" height="76" rx="20" fill="url(#gFace)"/>
    <g id="eye-l"><ellipse cx="165" cy="235" rx="14" ry="18" fill="#06B6D4" filter="url(#fGlow)"/><ellipse cx="159" cy="228" rx="4" ry="5" fill="white" opacity="0.55"/></g>
    <g id="eye-r"><ellipse cx="235" cy="235" rx="14" ry="18" fill="#06B6D4" filter="url(#fGlow)"/><ellipse cx="229" cy="228" rx="4" ry="5" fill="white" opacity="0.55"/></g>
    <g id="mouth-path"><path d="M 178 258 Q 200 278 222 258" fill="none" stroke="#06B6D4" stroke-width="4.5" stroke-linecap="round"/></g>
  </g>
</svg>
'''

st.markdown(
    f'<div style="text-align:center; margin-bottom:-1.5rem;">{ANIMATED_ICON}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<style>[data-testid="stImage"] { display:flex; justify-content:center; }</style>',
    unsafe_allow_html=True,
)
_, wcol, _ = st.columns([1, 2, 1])
with wcol:
    st.image(str(ASSETS / "wordmark.png"), use_container_width=True)

if "history" not in st.session_state:
    st.session_state.history = []


def check_connection():
    try:
        requests.get(OLLAMA_URL, timeout=2)
        return True
    except requests.exceptions.RequestException:
        return False


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if check_connection():
        st.markdown(
            '<div style="text-align:center;"><span class="tc-badge online">'
            '<span class="tc-dot"></span> Connecté au serveur d\'inférence</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="text-align:center;"><span class="tc-badge offline">'
            '<span class="tc-dot"></span> Déconnecté — démarrez Ollama</span></div>',
            unsafe_allow_html=True,
        )

for message in st.session_state.history:
    avatar = str(ASSETS / "icon.png") if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

if prompt := st.chat_input("Posez une question financière..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=str(ASSETS / "icon.png")):
        with st.spinner("Le modèle réfléchit..."):
            try:
                response = requests.post(
                    f"{OLLAMA_URL}/api/generate",
                    json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
                    timeout=120,
                )
                response.raise_for_status()
                answer = response.json()["response"]
            except requests.exceptions.RequestException as e:
                answer = f"Erreur de connexion au serveur d'inférence : {e}"
            st.write(answer)

    st.session_state.history.append({"role": "assistant", "content": answer})

st.markdown('<p class="tc-footer">TechCorp Industries — Assistant Financier propulsé par Phi-3.5-Financial</p>', unsafe_allow_html=True)
