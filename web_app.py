import streamlit as st

from src.speech import record_audio, speech_to_text
from src.nlp import analyze_sentence
from src.translator import translate_to_asl


st.set_page_config(
    page_title="SignBridge AI",
    page_icon="🤟",
    layout="centered"
)

st.title("🤟 SignBridge AI")
st.subheader("Speech → American Sign Language")

st.write(
    "Real-time speech-to-ASL translation using "
    "speech recognition, NLP, and sign video generation."
)

st.divider()

st.header("🎤 Speech Input")

if st.button("Start Speaking", use_container_width=True):

    with st.spinner("🎤 Listening..."):
        audio_file = record_audio()

    with st.spinner("🧠 Converting speech to text..."):
        text = speech_to_text(audio_file)

    st.success("Speech recognized!")

    st.header("📝 Recognized Speech")
    st.write(text)

    # NLP
    analysis = analyze_sentence(text)

    # ASL Translation
    sign_sequence = translate_to_asl(analysis)

    st.header("🤟 ASL Translation")
    st.write(" → ".join(sign_sequence))