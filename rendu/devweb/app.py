import streamlit as st
import requests

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "techcorp-financial"

st.set_page_config(page_title="TechCorp Financial Assistant", page_icon="💬")
st.title("💬 TechCorp Financial Assistant")

if "history" not in st.session_state:
    st.session_state.history = []


def check_connection():
    try:
        requests.get(OLLAMA_URL, timeout=2)
        return True
    except requests.exceptions.RequestException:
        return False


if check_connection():
    st.success("🟢 Connecté au serveur d'inférence (Ollama)")
else:
    st.error("🔴 Déconnecté — vérifiez que Ollama est démarré (`ollama serve`)")

st.divider()

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Posez une question financière..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
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
