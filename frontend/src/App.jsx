import { useCallback, useEffect, useRef, useState } from "react";
import {
  Mic,
  ArrowRight,
  RotateCcw,
  Play,
  Square,
} from "lucide-react";
import "./App.css";

const BACKEND_URL = "http://127.0.0.1:8000";

function App() {
  const [screen, setScreen] = useState("intro");

  const [listening, setListening] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
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
  const [normalizedWords, setNormalizedWords] =
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
    setErrorMessage("");
    try {
      if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error("Microphone access is not available in this browser.");
      }
      const stream =
        await navigator.mediaDevices.getUserMedia({
          audio: {
            noiseSuppression: { ideal: true },
            echoCancellation: { ideal: true },
            autoGainControl: { ideal: true },
          },
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
        setProcessing(true);

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
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || "Translation request failed.");
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

          setErrorMessage(error.message || "Could not connect to the SignBridge backend.");
        } finally {
          setProcessing(false);
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

      setErrorMessage(error.message || "Microphone access was denied or is unavailable.");
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
    setNormalizedWords([]);
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

    const words = recognizedText
      .replace(/[.,!?;:]/g, "")
      .split(/\s+/)
      .filter(Boolean);
    const mappedGlosses = translationData.sign_sequence || [];

    setUnderstandingWords(
      words.map((word) => ({ english: word, keep: true }))
    );
    setNormalizedWords(mappedGlosses);

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

  const getAvailableSigns = useCallback(() => {
    if (!translationData) {
      return [];
    }

    return translationData.signs || [];
  }, [translationData]);

  const getPlayableSigns = useCallback(() => {
    return getAvailableSigns().filter(
      (sign) => sign.found && sign.video
    );
  }, [getAvailableSigns]);

  const startASL = () => {
    const available = getPlayableSigns();

    if (available.length === 0) {
      return;
    }

    setVideoTransitioning(false);
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

  }, [currentSignIndex, getPlayableSigns, sequencePlaying]);

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
    setVideoTransitioning(false);
  };

  const newTranslation = () => {
    stopASL();

    clearAnimationTimers();

    setRecognizedText("");
    setTranslationData(null);
    setUnderstandingWords([]);
    setNormalizedWords([]);
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
          Speech → curated ASL glosses
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
              : processing
                ? "Transcribing speech and matching available sign resources…"
                : "Speak English to create a curated ASL gloss sequence with matching sign videos."}
          </p>

          {processing && <p className="processing-message" role="status">Processing your recording…</p>}
          {errorMessage && <p className="app-error" role="alert">{errorMessage}</p>}

          {!recognizedText && !processing &&
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
                  Speak clearly in English. Noise reduction is used when supported by your browser.
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
            Review the sentence analysis, meaning matches, controlled ASL rules, and available sign clips.
          </p>

          <div className="sentence-area">

            <div className="sentence-label">
              ANALYSIS AND ASL GLOSS MAPPING
            </div>

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

              {understandingStage === "filtering" &&
                normalizedWords.map((sign, index) => (
                    <span
                      key={`${sign}-${index}`}
                      className="word word-asl"
                    >
                      {sign}
                    </span>
                  ))}

              {understandingStage === "asl" &&
                (translationData?.sign_sequence || []).map(
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
                ? "APPLYING CURATED RULES"
                : "FINAL GLOSS SEQUENCE"}
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
const unresolvedSigns = signs.filter((sign) => !sign.found);

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
        SEQUENTIAL SIGN OUTPUT
      </div>


      <h2>
        Your translation is
        <br />

        <span>
          ready.
        </span>
      </h2>

      <p className="page-description">
        Resolved clips play in sequence. The pipeline shows how each word was analyzed and matched; its controlled gloss rules are not fluent ASL grammar.
      </p>

      <div className="transcript-summary" aria-label="Recognized English transcript">
        <strong>RECOGNIZED ENGLISH</strong>
        <p>{recognizedText || "No transcript is available."}</p>
      </div>

      <div className="gloss-summary" aria-label="Curated gloss sequence">
        <strong>GLOSS SEQUENCE</strong>
        <div>{(translationData?.sign_sequence || []).map((gloss, index) => <span className="gloss-chip" key={`${gloss}-${index}`}>{gloss}</span>)}</div>
      </div>

      {unresolvedSigns.length > 0 && (
        <p className="unresolved-notice" role="status">
          No sign video is available for: {unresolvedSigns.map((sign) => sign.gloss || sign.word).join(", " )}. These terms are omitted from playback.
        </p>
      )}

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

              onLoadedData={() => {
                if (sequencePlaying) {
                  setVideoTransitioning(false);
                }
              }}

              onError={() => setVideoTransitioning(false)}

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

      <details className="mapping-details pipeline-details">
        <summary>View the algorithm steps</summary>
        <div className="pipeline-list">
          <section className="pipeline-step">
            <strong>1. Speech recognition</strong>
            <p>{translationData?.text || recognizedText || "No recognized sentence."}</p>
          </section>
          <section className="pipeline-step">
            <strong>2. Text and grammar analysis</strong>
            <p>{(translationData?.analysis?.tokens || []).map((token) => `${token.surface} (${token.pos || "word"}${token.dependency ? `, ${token.dependency}` : ""})`).join(" · ") || "No token analysis available."}</p>
            <small>Sentence type: {translationData?.analysis?.sentence_type || "unknown"}</small>
          </section>
          <section className="pipeline-step">
            <strong>3. Lexical normalization</strong>
            <p>{(translationData?.analysis?.keywords || []).join(" → ") || "No normalized glosses available."}</p>
          </section>
          <section className="pipeline-step">
            <strong>4. Contextual meaning and synonym matching</strong>
            <p>Resource: {translationData?.semantic_mapping?.semantic_resource || "unknown"}</p>
            {(translationData?.semantic_mapping?.trace || []).map((item, index) => (
              <small className="semantic-trace-row" key={`${item.input}-${index}`}>
                {item.input} → {item.resolved_gloss || `unresolved (${(item.candidate_concepts || []).join(", ") || "no catalog candidate"})`} · {item.method}
                {item.confidence ? ` · ${(item.confidence * 100).toFixed(0)}%` : ""}
              </small>
            ))}
          </section>
          <section className="pipeline-step">
            <strong>5. Target-language transformation</strong>
            <p>{translationData?.target_transformation?.rule_set || "Controlled ASL rules"}: {(translationData?.target_transformation?.sequence || translationData?.sign_sequence || []).join(" → ")}</p>
            {(translationData?.target_transformation?.limitations || []).map((item, index) => (
              <small key={`limit-${index}`}>{item}</small>
            ))}
          </section>
          <section className="pipeline-step">
            <strong>6. Concept, sign, and resource resolution</strong>
            <p>{(translationData?.signs || []).map((sign) => `${sign.gloss}: ${sign.status}`).join(" · ") || "No resource checks available."}</p>
          </section>
          <section className="pipeline-step">
            <strong>7. Visual output</strong>
            <p>Available sign videos play in order; unresolved words and unavailable clips remain visible in the mapping.</p>
          </section>
        </div>
      </details>

      <details className="mapping-details">
        <summary>View concept and resource mapping</summary>
        <div className="mapping-list">
          {signs.map((sign, index) => (
            <div className="mapping-row" key={`${sign.gloss || sign.word}-${index}`}>
              <strong>{sign.gloss || sign.word}</strong>
              <span>{sign.concept_id || "No concept ID"}</span>
              <span>{sign.sign_id || "No sign ID"}</span>
              <span>{sign.status || (sign.found ? "resolved" : "unresolved")}</span>
            </div>
          ))}
        </div>
      </details>

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
