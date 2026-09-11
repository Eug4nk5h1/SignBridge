import streamlit as st

from src.speech import record_audio, speech_to_text
from src.nlp import analyze_sentence
from src.translator import translate_to_asl
from src.sign_library import get_sign


st.set_page_config(
    page_title="SignBridge AI",
    page_icon="🤟",
    layout="centered"
)

st.title("🤟 SignBridge AI")
st.subheader("Speech → American Sign Language")

st.write(
    "Translate spoken English into an ASL sign sequence "
    "using speech recognition and NLP."
)

st.divider()

# ----------------------------------------
# SPEECH INPUT
# ----------------------------------------

st.header("🎤 Speech Input")

if st.button("Start Speaking", use_container_width=True):

    # Speech recognition
    with st.spinner("🎤 Listening..."):
        audio_file = record_audio()

    with st.spinner("🧠 Converting speech to text..."):
        text = speech_to_text(audio_file)

    st.success("Speech recognized!")

    # ----------------------------------------
    # RECOGNIZED SPEECH
    # ----------------------------------------

    st.header("📝 Recognized Speech")
    st.write(text)

    # ----------------------------------------
    # NLP
    # ----------------------------------------

    analysis = analyze_sentence(text)

    # ----------------------------------------
    # ASL TRANSLATION
    # ----------------------------------------

    sign_sequence = translate_to_asl(analysis)

    st.header("🤟 ASL Translation")

    if sign_sequence:
        st.write(" → ".join(sign_sequence))
    else:
        st.warning("No ASL signs were detected.")

    # ----------------------------------------
    # ASL VIDEO OUTPUT
    # ----------------------------------------

    st.header("🎥 ASL Sign Output")

    for sign in sign_sequence:

        video_path = get_sign(sign)

        if video_path:
            st.subheader(sign)

            # Display video inside the webpage
            st.video(str(video_path))

        else:
            st.warning(
                f"No video available for: {sign}"
            )