import { useState } from 'react'
import './App.css'

function App() {
  const [isListening, setIsListening] = useState(false)

  return (
    <div className="app">

      {/* NAVIGATION */}
      <nav className="navbar">
        <a href="#home" className="brand">
          <span className="brand-mark">S</span>
          <span>SignBridge</span>
        </a>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#get-started">Get Started</a>
          <a href="#about">About</a>
        </div>

        <a href="#get-started" className="nav-button">
          Try it
        </a>
      </nav>


      {/* HOME */}
      <main>

        <section className="home" id="home">

          <div className="home-left">

            <div className="eyebrow">
              AMERICAN SIGN LANGUAGE
            </div>

            <h1>
              Speak naturally.
              <br />
              <em>See it in sign.</em>
            </h1>

            <p className="intro">
              SignBridge helps bridge communication by turning
              spoken language into American Sign Language,
              one sentence at a time.
            </p>

            <div className="home-buttons">
              <a href="#get-started" className="main-button">
                Start translating
                <span>→</span>
              </a>

              <a href="#about" className="text-button">
                How it works
              </a>
            </div>

            <div className="small-note">
              No account required · Simple to use
            </div>

          </div>


          <div className="home-right">

            <div className="paper-card">

              <div className="card-heading">
                <span>LIVE TRANSLATION</span>
                <span className="live-dot"></span>
              </div>

              <div className="example-text">
                <span className="quotation">“</span>

                <p>
                  Hello, how are you?
                </p>
              </div>

              <div className="divider"></div>

              <div className="sign-preview">

                <div className="hand-illustration">
                  <span>🤟</span>
                </div>

                <div>
                  <small>AMERICAN SIGN LANGUAGE</small>
                  <strong>HELLO</strong>
                </div>

              </div>

              <div className="card-footer">
                <span>Speech</span>
                <span>→</span>
                <span>ASL</span>
              </div>

            </div>

          </div>

        </section>


        {/* GET STARTED */}
        <section className="translator" id="get-started">

          <div className="section-intro">

            <div>
              <div className="eyebrow">
                GET STARTED
              </div>

              <h2>
                Let's translate.
              </h2>
            </div>

            <p>
              Press the microphone and speak your sentence.
              Your translation will appear on the right.
            </p>

          </div>


          <div className="translator-workspace">

            {/* INPUT */}

            <div className="workspace-panel">

              <div className="workspace-label">
                <span>YOUR SPEECH</span>
                <span className="ready">
                  <i></i>
                  {isListening ? 'Listening' : 'Ready'}
                </span>
              </div>

              <div className="speech-content">

                <span className="large-quote">
                  “
                </span>

                <p className="placeholder-text">
                  {isListening
                    ? 'Listening for your voice...'
                    : 'Your spoken words will appear here.'}
                </p>

              </div>

              <button
                className={`record-button ${isListening ? 'recording' : ''}`}
                onClick={() => setIsListening(!isListening)}
              >
                <span className="record-circle">
                  {isListening ? '■' : '●'}
                </span>

                {isListening
                  ? 'Stop listening'
                  : 'Start speaking'}
              </button>

            </div>


            <div className="workspace-arrow">
              →
            </div>


            {/* OUTPUT */}

            <div className="workspace-panel output">

              <div className="workspace-label">
                <span>ASL TRANSLATION</span>
                <span className="asl-label">ASL</span>
              </div>

              <div className="sign-video">

                <div className="video-inner">
                  <span>🤟</span>

                  <button className="video-play">
                    ▶
                  </button>
                </div>

              </div>

              <div className="translation-caption">
                <small>TRANSLATED SIGN</small>
                <strong>Waiting for speech...</strong>
              </div>

            </div>

          </div>

        </section>


        {/* HOW IT WORKS */}

        <section className="how-section">

          <div className="eyebrow">
            HOW IT WORKS
          </div>

          <h2>
            Three simple steps.
          </h2>

          <div className="steps">

            <div className="step">
              <span className="step-number">01</span>

              <div>
                <h3>Speak</h3>
                <p>
                  Use your microphone to say whatever
                  you want to communicate.
                </p>
              </div>
            </div>


            <div className="step">
              <span className="step-number">02</span>

              <div>
                <h3>Process</h3>
                <p>
                  Your speech is converted into text and
                  processed by the translation system.
                </p>
              </div>
            </div>


            <div className="step">
              <span className="step-number">03</span>

              <div>
                <h3>Sign</h3>
                <p>
                  The corresponding American Sign Language
                  signs are displayed for you.
                </p>
              </div>
            </div>

          </div>

        </section>


        {/* ABOUT */}

        <section className="about" id="about">

          <div className="about-heading">

            <div className="eyebrow">
              ABOUT SIGNBRIDGE
            </div>

            <h2>
              Technology should
              <br />
              <em>bring people closer.</em>
            </h2>

          </div>


          <div className="about-text">

            <p>
              Communication can become difficult when people
              use different languages or communication methods.
              SignBridge explores how technology can help make
              that gap a little smaller.
            </p>

            <p>
              The system takes spoken language, converts it into
              text, processes the sentence, and presents the
              corresponding American Sign Language signs through
              visual demonstrations.
            </p>

            <div className="about-line"></div>

            <span>
              Built as a project with accessibility in mind.
            </span>

          </div>

        </section>


        {/* FINAL CTA */}

        <section className="final-section">

          <div className="final-inner">

            <div>
              <div className="eyebrow">
                SIGNBRIDGE
              </div>

              <h2>
                Ready to give it a try?
              </h2>
            </div>

            <a href="#get-started" className="main-button">
              Start translating
              <span>→</span>
            </a>

          </div>

        </section>

      </main>


      {/* FOOTER */}

      <footer>

        <div className="brand">
          <span className="brand-mark">S</span>
          <span>SignBridge</span>
        </div>

        <span>
          Speech → American Sign Language
        </span>

        <span>
          © 2026
        </span>

      </footer>

    </div>
  )
}

export default App