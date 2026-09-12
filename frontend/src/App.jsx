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

  const [playingIndex, setPlayingIndex] = useState(-1);
  const [sequencePlaying, setSequencePlaying] = useState(false);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const videoRefs = useRef([]);

  const animationTimersRef = useRef([]);

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

  const startASL = () => {
    if (sequencePlaying) return;

    const signs = getAvailableSigns();

    const firstAvailableIndex =
      signs.findIndex(
        (sign) => sign.found && sign.video
      );

    if (firstAvailableIndex === -1) {
      return;
    }

    setSequencePlaying(true);
    setPlayingIndex(firstAvailableIndex);

    const video =
      videoRefs.current[firstAvailableIndex];

    if (video) {
      video.currentTime = 0;

      video.play().catch((error) => {
        console.error(
          "Video playback failed:",
          error
        );
      });
    }
  };

  const handleVideoEnded = (index) => {
    const signs = getAvailableSigns();

    /*
      Find the next available video.
      Missing videos are skipped.
    */
    let nextIndex = -1;

    for (
      let i = index + 1;
      i < signs.length;
      i++
    ) {
      if (
        signs[i].found &&
        signs[i].video
      ) {
        nextIndex = i;
        break;
      }
    }

    if (nextIndex !== -1) {
      setTimeout(() => {
        setPlayingIndex(nextIndex);

        const nextVideo =
          videoRefs.current[nextIndex];

        if (nextVideo) {
          nextVideo.currentTime = 0;

          nextVideo.play().catch(
            (error) => {
              console.error(
                "Video playback failed:",
                error
              );
            }
          );
        }
      }, 600);
    } else {
      /*
        Entire sequence finished.
      */
      setPlayingIndex(-1);
      setSequencePlaying(false);
    }
  };

  const stopASL = () => {
    videoRefs.current.forEach(
      (video) => {
        if (video) {
          video.pause();
        }
      }
    );

    setPlayingIndex(-1);
    setSequencePlaying(false);
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

  /* =========================
     INTRO SCREEN
  ========================= */

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

        <header>
          <div className="brand">
            <span>🤟</span>
            <strong>SignBridge</strong>
          </div>

          <div className="page-number">
            01 / 03
          </div>
        </header>

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
            Speak in English and SignBridge
            will transform your speech into
            American Sign Language.
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

              <div className="listening-orb">

                <div className="sound-wave wave-one"></div>
                <div className="sound-wave wave-two"></div>
                <div className="sound-wave wave-three"></div>

                <Mic size={34} />
              </div>

              <h3>
                LISTENING...
              </h3>

              <p>
                SignBridge is listening
                to your speech.
              </p>

              <div className="audio-bars">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
              </div>

              <button
                className="secondary-button"
                onClick={stopListening}
              >
                <Square
                  size={15}
                  fill="currentColor"
                />
                Stop Listening
              </button>

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

        <header>
          <div className="brand">
            <span>🤟</span>
            <strong>SignBridge</strong>
          </div>

          <div className="page-number">
            02 / 03
          </div>
        </header>

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

  return (
    <div className="app">

      <header>
        <div className="brand">
          <span>🤟</span>
          <strong>SignBridge</strong>
        </div>

        <div className="page-number">
          03 / 03
        </div>
      </header>

      <main className="output-page">

        <div className="page-label">
          ASL OUTPUT
        </div>

        <h2>
          Your translation is
          <br />
          <span>ready.</span>
        </h2>

        <p className="page-description">
          Follow the signs from left to right.
        </p>

        <div className="video-sequence">

          {signs.map((sign, index) => (

            <div
              className={`video-card ${
                playingIndex === index
                  ? "video-active"
                  : ""
              } ${
                !sign.found
                  ? "video-missing"
                  : ""
              }`}
              key={`${sign.word}-${index}`}
            >

              <div className="video-word">
                {sign.word}
              </div>

              {sign.found &&
              sign.video ? (
                <video
                  ref={(element) => {
                    videoRefs.current[index] =
                      element;
                  }}
                  src={`${BACKEND_URL}${sign.video}`}
                  muted
                  playsInline
                  preload="metadata"
                  onEnded={() =>
                    handleVideoEnded(index)
                  }
                />
              ) : (
                <div className="no-video">

                  <div className="no-video-icon">
                    🎥
                  </div>

                  <p>
                    No video available
                  </p>

                  <small>
                    Working on it
                  </small>

                </div>
              )}

              {playingIndex === index && (
                <div className="playing-indicator">
                  <span></span>
                  PLAYING
                </div>
              )}

            </div>

          ))}

        </div>

        <div className="output-actions">

          {!sequencePlaying &&
            playingIndex === -1 && (
              <button
                className="primary-button start-asl"
                onClick={startASL}
                disabled={
                  !signs.some(
                    (sign) =>
                      sign.found &&
                      sign.video
                  )
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

          {!sequencePlaying &&
            playingIndex === -1 && (
              <button
                className="secondary-button"
                onClick={newTranslation}
              >
                <RotateCcw size={17} />
                New Translation
              </button>
            )}

          {sequencePlaying && (
            <div className="playing-status">
              <span className="status-dot"></span>
              Playing ASL sequence...
            </div>
          )}

        </div>

        {!sequencePlaying &&
          playingIndex === -1 && (
            <div className="output-complete">
              <Check size={16} />
              Each sign plays once.
              Press Start ASL again to replay.
            </div>
          )}

      </main>

      <footer className="steps">

        <div className="step">
          <b>01</b>
          <span>Speak</span>
        </div>

        <div className="step-line"></div>

        <div className="step">
          <b>02</b>
          <span>Understand</span>
        </div>

        <div className="step-line"></div>

        <div className="step active">
          <b>03</b>
          <span>Sign</span>
        </div>

      </footer>

    </div>
  );
}

export default App;