import { Mic } from "lucide-react";
import "./App.css";

function App() {
  return (
    <div className="app">

      {/* Intro */}
      <section className="intro-screen">

        <div className="intro-symbol">
          <span>🤟</span>
        </div>

        <div className="intro-title">
          <h1>SIGNBRIDGE</h1>
          <p>AI</p>
        </div>

        <div className="intro-line"></div>

        <p className="intro-subtitle">
          Speech → American Sign Language
        </p>

      </section>


      {/* Main Page */}
      <section className="home-screen">

        <div className="top-bar">
          <div className="brand">
            <span className="brand-symbol">🤟</span>
            <span>SignBridge</span>
          </div>

          <div className="system-status">
            <span></span>
            System ready
          </div>
        </div>


        <div className="hero">

          <p className="eyebrow">
            SPEECH TO SIGN LANGUAGE
          </p>

          <h2>
            Communication
            <br />
            <span>without barriers.</span>
          </h2>

          <p className="description">
            Speak naturally in English.
            <br />
            SignBridge AI will transform your words
            into American Sign Language.
          </p>


          {/* Microphone */}
          <div className="mic-area">

            <div className="pulse pulse-one"></div>
            <div className="pulse pulse-two"></div>
            <div className="pulse pulse-three"></div>

            <button className="mic-button">
              <Mic size={42} strokeWidth={1.8} />
            </button>

          </div>


          <p className="speak-text">
            TAP TO SPEAK
          </p>

          <p className="hint">
            Your microphone will activate when you tap
          </p>

        </div>


        <div className="bottom-info">
          <div>
            <strong>01</strong>
            <span>Speak</span>
          </div>

          <div className="bottom-line"></div>

          <div>
            <strong>02</strong>
            <span>Understand</span>
          </div>

          <div className="bottom-line"></div>

          <div>
            <strong>03</strong>
            <span>Sign</span>
          </div>
        </div>

      </section>

    </div>
  );
}

export default App;