import streamlit as st
import google.generativeai as genai
import os

# ==============================================================================
# PENGATURAN ANTARMUKA STREAMLIT
# ==============================================================================

# Konfigurasi halaman
st.set_page_config(
    page_title="Chatbot Apoteker",
    page_icon="💊",
    layout="centered"
)

st.title("💊 Chatbot Apoteker")
st.markdown("Tanyakan kepada saya tentang obat atau penyakit, saya akan mencoba membantu. "
            "Saya adalah model AI dan jawaban saya tidak menggantikan saran medis profesional.")

# Menggunakan sidebar untuk API Key (lebih aman)
with st.sidebar:
    st.header("Konfigurasi")
    api_key = st.text_input("Masukkan API Key Gemini Anda:", type="password")

# ==============================================================================
# KONTEKS AWAL CHATBOT
# ==============================================================================

INITIAL_CHATBOT_CONTEXT = [
    {
        "role": "user",
        "parts": ["Kamu adalah ahli apoteker. Tuliskan obat apa yang di inginkan untuk menyembuhkan penyakit anda. Jawaban singkat dan jelas. Tolak pertanyaan selain tentang obat."]
    },
    {
        "role": "model",
        "parts": ["Baik! saya akan menjawab pertanyaan anda tentang Obat."]
    }
]

# ==============================================================================
# FUNGSI UTAMA CHATBOT
# ==============================================================================

# Inisialisasi riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat pesan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Cek dan konfigurasi API Key
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Inisialisasi model
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config=genai.types.GenerationConfig(
                temperature=0.4,
                max_output_tokens=500
            )
        )
        
        # Inisialisasi sesi chat
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=INITIAL_CHATBOT_CONTEXT)
        
        # Minta input pengguna
        if prompt := st.chat_input("Tanyakan sesuatu..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Sedang membalas..."):
                    try:
                        response = st.session_state.chat_session.send_message(prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"Maaf, terjadi kesalahan: {e}. Pastikan API Key valid.")
                        
    except Exception as e:
        st.error(f"Kesalahan konfigurasi API: {e}. Pastikan API Key Anda benar.")
        
else:
    st.warning("Silakan masukkan API Key Gemini Anda di sidebar untuk memulai.")
