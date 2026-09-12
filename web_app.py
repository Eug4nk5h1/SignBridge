import streamlit as st

from src.speech import record_audio, speech_to_text
from src.nlp import analyze_sentence
from src.translator import translate_to_asl
from src.sign_library import get_sign


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="SignBridge AI",
    page_icon="🤟",
    layout="wide"
)


# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 25px;
        font-weight: bold;
        margin-top: 20px;
    }

    .translation-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #cccccc;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 15px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown(
    '<div class="main-title">🤟 SignBridge AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Real-Time Speech → American Sign Language Translation'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -------------------------------------------------
# SPEECH INPUT
# -------------------------------------------------

st.markdown(
    '<div class="section-title">🎤 Speech Input</div>',
    unsafe_allow_html=True
)

st.write(
    "Click the button and speak clearly in English."
)

if st.button(
    "🎤 Start Speaking",
    use_container_width=True
):

    # ---------------------------------------------
    # RECORD AUDIO
    # ---------------------------------------------

    with st.spinner("🎤 Listening..."):
        audio_file = record_audio()

    # ---------------------------------------------
    # WHISPER
    # ---------------------------------------------

    with st.spinner("🧠 Converting speech to text..."):
        text = speech_to_text(audio_file)

    st.success("Speech recognized successfully!")


    # ---------------------------------------------
    # RECOGNIZED SPEECH
    # ---------------------------------------------

    st.markdown(
        '<div class="section-title">📝 Recognized Speech</div>',
        unsafe_allow_html=True
    )

    st.info(text)


    # ---------------------------------------------
    # NLP
    # ---------------------------------------------

    analysis = analyze_sentence(text)


    # ---------------------------------------------
    # ASL TRANSLATION
    # ---------------------------------------------

    sign_sequence = translate_to_asl(analysis)

    st.markdown(
        '<div class="section-title">🤟 ASL Translation</div>',
        unsafe_allow_html=True
    )

    if sign_sequence:

        translation = " → ".join(sign_sequence)

        st.markdown(
            f'<div class="translation-box">{translation}</div>',
            unsafe_allow_html=True
        )

    else:

        st.warning(
            "No ASL signs were detected for this input."
        )


    # ---------------------------------------------
    # SIGN VIDEOS
    # ---------------------------------------------

    st.markdown(
        '<div class="section-title">🎥 ASL Sign Output</div>',
        unsafe_allow_html=True
    )

    if sign_sequence:

        columns = st.columns(
            min(len(sign_sequence), 3)
        )

        for index, sign in enumerate(sign_sequence):

            video_path = get_sign(sign)

            with columns[index % len(columns)]:

                st.subheader(sign)

                if video_path:

                    st.video(str(video_path))

                else:

                    st.warning(
                        f"Video not available for {sign}"
                    )

    else:

        st.info(
            "Sign videos will appear here after translation."
        )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "SignBridge AI • Speech-to-ASL Translation System"
)