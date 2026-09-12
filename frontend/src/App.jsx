import { useEffect, useRef, useState } from "react";
import {
  Mic,
  ArrowRight,
  RotateCcw,
  Play,
  Check,
  Square,
} from "lucide-react";
import "./App.css";

const BACKEND_URL = "http://127.0.0.1:8000";

function App() {
  const [screen, setScreen] = useState("intro");

  const [listening, setListening] = useState(false);
  const [recognizedText, setRecognizedText] = useState("");

  const [translationData, setTranslationData] = useState(null);

  /*
    Page 2 animation states:

    "english"   → original sentence
    "filtering" → unnecessary words disappear
    "asl"       → ASL-oriented sequence appears in same area
  */
  const [understandingStage, setUnderstandingStage] =
    useState("english");

  const [understandingWords, setUnderstandingWords] =
    useState([]);

  const [sequencePlaying, setSequencePlaying] = useState(false);

  const [currentSignIndex, setCurrentSignIndex] = useState(0);

  const singleVideoRef = useRef(null);
  const sequenceTimerRef = useRef(null);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const animationTimersRef = useRef([]);
  const [videoTransitioning, setVideoTransitioning] = useState(false);

  /* =========================
     INTRO
  ========================= */

  useEffect(() => {
    if (screen !== "intro") return;

    const timer = setTimeout(() => {
      setScreen("speak");
    }, 4200);

    return () => clearTimeout(timer);
  }, [screen]);

  /* =========================
     SPEECH INPUT
  ========================= */

  const startListening = async () => {
    try {
      const stream =
        await navigator.mediaDevices.getUserMedia({
          audio: true,
        });

      const recorder = new MediaRecorder(stream);

      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        setListening(false);

        stream
          .getTracks()
          .forEach((track) => track.stop());

        const audioBlob = new Blob(
          audioChunksRef.current,
          {
            type: "audio/webm",
          }
        );

        const formData = new FormData();

        formData.append(
          "file",
          audioBlob,
          "recording.webm"
        );

        try {
          const response = await fetch(
            `${BACKEND_URL}/translate`,
            {
              method: "POST",
              body: formData,
            }
          );

          if (!response.ok) {
            throw new Error(
              "Backend request failed"
            );
          }

          const data = await response.json();

          console.log(
            "SignBridge backend response:",
            data
          );

          setRecognizedText(data.text);
          setTranslationData(data);
        } catch (error) {
          console.error(
            "Translation error:",
            error
          );

          alert(
            "Could not connect to SignBridge AI backend."
          );
        }
      };

      recorder.start();

      setListening(true);

      console.log("🎤 Recording started");
    } catch (error) {
      console.error(
        "Microphone error:",
        error
      );

      alert(
        "Microphone access was denied or is unavailable."
      );
    }
  };

  const stopListening = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state !== "inactive"
    ) {
      mediaRecorderRef.current.stop();
    }
  };

  const sayAgain = () => {
    setRecognizedText("");
    setTranslationData(null);
    setUnderstandingWords([]);
    setUnderstandingStage("english");

    startListening();
  };

  /* =========================
     PAGE 2 PREPARATION
     ========================= */

  const clearAnimationTimers = () => {
    animationTimersRef.current.forEach(
      (timer) => clearTimeout(timer)
    );

    animationTimersRef.current = [];
  };

  useEffect(() => {
    return () => {
      clearAnimationTimers();
    };
  }, []);

  const continueToUnderstanding = () => {
    if (!recognizedText || !translationData) {
      return;
    }

    clearAnimationTimers();

    /*
      Use the REAL sentence returned by Whisper.
    */
    const words = recognizedText
      .replace(/[.,!?;:]/g, "")
      .split(/\s+/)
      .filter(Boolean);

    /*
      Backend translation result.

      Example:

      English:
      "Hello I am going to college"

      ASL:
      ["HELLO", "I", "GO", "COLLEGE"]
    */
    const aslSequence =
      translationData.sign_sequence || [];

    /*
      Words that actually survive the AI
      translation.

      We compare the normalized English words
      against the ASL sequence.
    */
    const meaningfulWords = [];

    words.forEach((word) => {
      const normalized = word.toUpperCase();

      const existsInASL =
        aslSequence.includes(normalized);

      /*
        Special English → ASL mappings.
        These allow words such as "going"
        to visually become "GO".
      */
      const lemmaMatch =
        normalized === "GOING" &&
        aslSequence.includes("GO");

      const shouldKeep =
        existsInASL || lemmaMatch;

      meaningfulWords.push({
        english: word,
        normalized,
        keep: shouldKeep,
      });
    });

    /*
      If the backend generated signs that do not
      exactly match the English words, the animation
      still has a meaningful filtering stage.
    */
    setUnderstandingWords(
      meaningfulWords
    );

    setUnderstandingStage("english");

    /*
      STAGE 1
      Show complete English sentence.
    */

    const timer1 = setTimeout(() => {
      setUnderstandingStage("filtering");
    }, 1300);

    /*
      STAGE 2
      Let unnecessary words disappear.
    */

    const timer2 = setTimeout(() => {
      setUnderstandingStage("asl");
    }, 3000);

    /*
      STAGE 3
      Replace the remaining representation
      with the actual ASL sequence.
    */

    animationTimersRef.current = [
      timer1,
      timer2,
    ];

    setScreen("understand");
  };

  /* =========================
     PAGE 3
     ASL VIDEO PLAYBACK
  ========================= */

  const getAvailableSigns = () => {
    if (!translationData) {
      return [];
    }

    return translationData.signs || [];
  };

  const getPlayableSigns = () => {
    return getAvailableSigns().filter(
      (sign) => sign.found && sign.video
    );
  };

  const startASL = () => {
    const available = getPlayableSigns();

    if (available.length === 0) {
      return;
    }

    setCurrentSignIndex(0);
    setSequencePlaying(true);
  };

  const handleVideoEnded = () => {
    const available = getPlayableSigns();

    const nextIndex = currentSignIndex + 1;

    if (nextIndex < available.length) {
      if (sequenceTimerRef.current) {
        clearTimeout(sequenceTimerRef.current);
      }

      setVideoTransitioning(true);

      sequenceTimerRef.current = setTimeout(() => {
        setCurrentSignIndex(nextIndex);
        setVideoTransitioning(false);
      }, 350);

      return;
    }

    setSequencePlaying(false);
  };

  useEffect(() => {
    if (!sequencePlaying) {
      return;
    }

    const available = getPlayableSigns();
    const currentSign = available[currentSignIndex];

    if (!currentSign) {
      return;
    }

    const video = singleVideoRef.current;

    if (!video) {
      return;
    }

    video.src = `${BACKEND_URL}${currentSign.video}`;
    video.load();

    const playVideo = async () => {
      try {
        await video.play();
      } catch (error) {
        console.error("Video playback failed:", error);
      }
    };

    playVideo();

  }, [currentSignIndex, sequencePlaying]);

  const stopASL = () => {
    if (sequenceTimerRef.current) {
      clearTimeout(sequenceTimerRef.current);
      sequenceTimerRef.current = null;
    }

    const video = singleVideoRef.current;

    if (video) {
      video.pause();
      video.removeAttribute("src");
      video.load();
    }

    setSequencePlaying(false);
    setCurrentSignIndex(0);
  };

  const newTranslation = () => {
    stopASL();

    clearAnimationTimers();

    setRecognizedText("");
    setTranslationData(null);
    setUnderstandingWords([]);
    setUnderstandingStage("english");

    setScreen("speak");
  };

  /* ==================== */

  if (screen === "intro") {
    return (
      <div className="intro-screen">
        <div className="intro-hand">
          🤟
        </div>

        <h1>SIGNBRIDGE</h1>

        <div className="intro-ai">
          AI
        </div>

        <div className="intro-divider"></div>

        <p>
          Speech → American Sign Language
        </p>
      </div>
    );
  }

  /* =========================
     PAGE 1
     SPEAK
  ========================= */

  if (screen === "speak") {
    return (
      <div className="app">

        <div className="page-top">
          <div className="brand">
            <span>🤟</span>
            <strong>SignBridge</strong>
          </div>

          <div className="page-number">
            01 / 03
          </div>
        </div>

        <main className="page">

          <div className="page-label">
            SPEECH INPUT
          </div>

          <h2>
            Speak naturally.
            <br />
            <span>
              We'll handle the rest.
            </span>
          </h2>

          <p className="page-description">
            {listening
              ? "SignBridge is listening to you."
              : "Speak in English and SignBridge will transform your speech into American Sign Language."}
          </p>

          {!recognizedText &&
            !listening && (
              <>
                <div className="mic-container">

                  <div className="ring ring-one"></div>
                  <div className="ring ring-two"></div>
                  <div className="ring ring-three"></div>

                  <button
                    className="mic-button"
                    onClick={startListening}
                  >
                    <Mic size={34} />
                  </button>

                </div>

                <div className="mic-label">
                  TAP TO SPEAK
                </div>

                <div className="small-text">
                  Speak clearly in English
                </div>
              </>
            )}

          {listening && (
            <div className="listening">

              <button
                className="listening-orb"
                onClick={stopListening}
                aria-label="Stop recording"
              >
                <div className="sound-wave wave-one"></div>
                <div className="sound-wave wave-two"></div>
                <div className="sound-wave wave-three"></div>

                <Mic size={34} />
              </button>

              <div className="audio-bars">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
              </div>

            </div>
          )}

          {recognizedText &&
            !listening && (
              <div className="recognized">

                <div className="recognized-label">
                  RECOGNIZED SPEECH
                </div>

                <div className="speech-box">
                  {recognizedText}
                </div>

                <div className="action-row">

                  <button
                    className="secondary-button"
                    onClick={sayAgain}
                  >
                    <RotateCcw size={17} />
                    Say Again
                  </button>

                  <button
                    className="primary-button"
                    onClick={
                      continueToUnderstanding
                    }
                  >
                    Continue
                    <ArrowRight size={18} />
                  </button>

                </div>

              </div>
            )}

        </main>

        <footer className="steps">

          <div className="step active">
            <b>01</b>
            <span>Speak</span>
          </div>

          <div className="step-line"></div>

          <div className="step">
            <b>02</b>
            <span>Understand</span>
          </div>

          <div className="step-line"></div>

          <div className="step">
            <b>03</b>
            <span>Sign</span>
          </div>

        </footer>

      </div>
    );
  }

  /* =========================
     PAGE 2
     UNDERSTANDING
  ========================= */

  if (screen === "understand") {
    return (
      <div className="app">

        <div className="page-top">
          <div className="brand">
            <span>🤟</span>
            <strong>SignBridge</strong>
          </div>

          <div className="page-number">
            02 / 03
          </div>
        </div>

        <main className="understand-page">

          <div className="page-label">
            SENTENCE UNDERSTANDING
          </div>

          <h2>
            Understanding
            <br />
            <span>
              your sentence.
            </span>
          </h2>

          <p className="page-description">
            SignBridge identifies the meaningful
            parts of your sentence and prepares
            them for ASL.
          </p>

          <div className="sentence-area">

            <div className="sentence-label">
              AI LANGUAGE TRANSFORMATION
            </div>

            {/*
              THIS IS THE IMPORTANT PART.

              There is ONLY ONE word container.

              English → filtering → ASL

              We are NOT creating a separate
              ASL preview underneath.
            */}

            <div
              className={`word-container transformation-stage-${understandingStage}`}
            >

              {understandingStage !== "asl" &&
                understandingWords.map(
                  (item, index) => (
                    <span
                      key={`${item.english}-${index}`}
                      className={`word word-${understandingStage} ${
                        item.keep
                          ? "word-meaningful"
                          : "word-support"
                      }`}
                    >
                      {item.english}
                    </span>
                  )
                )}

              {understandingStage === "asl" &&
                (translationData?.sign_sequence ||
                  []).map(
                  (sign, index) => (
                    <span
                      key={`${sign}-${index}`}
                      className="word word-asl"
                      style={{
                        animationDelay: `${
                          index * 0.12
                        }s`,
                      }}
                    >
                      {sign}
                    </span>
                  )
                )}

            </div>

          </div>

          <div className="transformation-line">

            <div></div>

            <span>
              {understandingStage ===
              "english"
                ? "READING SENTENCE"
                : understandingStage ===
                  "filtering"
                ? "IDENTIFYING MEANING"
                : "ASL REPRESENTATION"}
            </span>

            <div></div>

          </div>

          <button
            className="primary-button continue-understanding"
            onClick={() =>
              setScreen("output")
            }
            disabled={
              understandingStage !== "asl"
            }
          >
            View ASL Output
            <ArrowRight size={18} />
          </button>

        </main>

        <footer className="steps">

          <div className="step">
            <b>01</b>
            <span>Speak</span>
          </div>

          <div className="step-line"></div>

          <div className="step active">
            <b>02</b>
            <span>Understand</span>
          </div>

          <div className="step-line"></div>

          <div className="step">
            <b>03</b>
            <span>Sign</span>
          </div>

        </footer>

      </div>
    );
  }

/* =========================
   PAGE 3
   ASL OUTPUT
========================= */

const signs = getAvailableSigns();

const availableSigns = signs.filter(
  (sign) =>
    sign.found &&
    sign.video
);

const currentSign =
  availableSigns[currentSignIndex];

return (
  <div className="app">

    {/* =========================
        TOP BAR
    ========================= */}

    <div className="page-top">

      <div className="brand">

        <span>🤟</span>

        <strong>
          SignBridge
        </strong>

      </div>

      <div className="page-number">
        03 / 03
      </div>

    </div>


    {/* =========================
        MAIN OUTPUT
    ========================= */}

    <main className="output-page">

      <div className="page-label">
        ASL OUTPUT
      </div>


      <h2>
        Your translation is
        <br />

        <span>
          ready.
        </span>
      </h2>

      {/* =========================
          SINGLE SIGN
      ========================= */}

      {currentSign && (

        <div className="single-sign-view">


          {/* CURRENT WORD */}

        <div
          className={`single-video-container ${
            sequencePlaying ? "video-active" : ""
          } ${videoTransitioning ? "video-transitioning" : ""}`}
        >

          <div className="video-side-label video-word">
            {currentSign.word}
          </div>

          <div className="video-side-label video-progress">
            SIGN {currentSignIndex + 1} / {availableSigns.length}
          </div>

            <video

              ref={singleVideoRef}

              src={`${BACKEND_URL}${currentSign.video}`}

              muted

              playsInline

              preload="auto"

              controls={false}

              onEnded={
                handleVideoEnded
              }

            />


            {/* PLAYING INDICATOR */}

            {sequencePlaying && (

              <div className="playing-indicator">

                <span></span>

                PLAYING

              </div>

            )}

          </div>

        </div>

      )}


      {/* =========================
          NO VIDEO
      ========================= */}

      {!currentSign && (

        <div className="no-signs">

          No ASL videos are currently
          available.

        </div>

      )}


      {/* =========================
          BUTTONS
      ========================= */}

      <div className="output-actions">


        {!sequencePlaying && (

          <button

            className="primary-button start-asl"

            onClick={startASL}

            disabled={
              availableSigns.length === 0
            }

          >

            <Play
              size={18}
              fill="currentColor"
            />

            Start ASL

          </button>

        )}


        {sequencePlaying && (

          <button

            className="secondary-button"

            onClick={stopASL}

          >

            <Square
              size={16}
              fill="currentColor"
            />

            Stop

          </button>

        )}


        {!sequencePlaying && (

          <button

            className="secondary-button"

            onClick={newTranslation}

          >

            <RotateCcw
              size={17}
            />

            New Translation

          </button>

        )}

      </div>

    </main>


    {/* =========================
        BOTTOM STEPS
    ========================= */}

    <footer className="steps">

      <div className="step">

        <b>01</b>

        <span>
          Speak
        </span>

      </div>


      <div className="step-line"></div>


      <div className="step">

        <b>02</b>

        <span>
          Understand
        </span>

      </div>


      <div className="step-line"></div>


      <div className="step active">

        <b>03</b>

        <span>
          Sign
        </span>

      </div>

    </footer>

  </div>
);
}
export default App;