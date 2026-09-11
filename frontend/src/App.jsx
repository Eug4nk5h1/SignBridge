import { useState } from 'react'
import './App.css'

function App() {
  const [isListening, setIsListening] = useState(false)

  return (
    <div className="app">

      {/* Navigation */}
      <nav className="navbar">
        <a href="#home" className="brand">
          <div className="brand-icon">🤟</div>
          <span>SignBridge</span>
        </a>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#get-started">Get Started</a>
          <a href="#about">About</a>
        </div>

        <a href="#get-started" className="nav-button">
          Get Started
        </a>
      </nav>


      {/* HOME */}
      <main>

        <section className="hero-section" id="home">

          <div className="hero-content">

            <div className="tag">
              <span>●</span> AMERICAN SIGN LANGUAGE
            </div>

            <h1>
              Breaking barriers,
              <br />
              <span>one sign at a time.</span>
            </h1>

            <p>
              SignBridge transforms spoken words into American Sign
              Language, helping create more accessible and inclusive
              communication for everyone.
            </p>

            <div className="hero-actions">

              <a
                href="#get-started"
                className="primary-button"
              >
                <span className="mic-icon">🎙</span>
                Start Translating
              </a>

              <a href="#about" className="secondary-button">
                Learn More <span>→</span>
              </a>

            </div>

          </div>


          {/* Hero visual */}

          <div className="hero-visual">

            <div className="visual-glow"></div>

            <div className="sign-card main-card">

              <div className="card-label">
                ASL TRANSLATION
              </div>

              <div className="sign-placeholder">
                <span>🤟</span>
              </div>

              <div className="card-word">
                HELLO
              </div>

              <div className="card-caption">
                American Sign Language
              </div>

            </div>


            <div className="floating-card top-card">

              <span className="floating-icon">🎙</span>

              <div>
                <strong>Speech detected</strong>
                <small>Ready to translate</small>
              </div>

            </div>


            <div className="floating-card bottom-card">

              <span>✓</span>

              <div>
                <strong>Real-time</strong>
                <small>Translation</small>
              </div>

            </div>

          </div>

        </section>


        {/* GET STARTED */}

        <section className="translator-section" id="get-started">

          <div className="translator-header">

            <div>

              <div className="tag">
                GET STARTED
              </div>

              <h2>
                Your words.
                <br />
                Their language.
              </h2>

            </div>

            <p>
              Speak naturally and let SignBridge convert your
              speech into American Sign Language.
            </p>

          </div>


          <div className="translator-box">

            {/* Speech input */}

            <div className="input-panel">

              <div className="panel-top">

                <span>
                  YOUR SPEECH
                </span>

                <span className="status">
                  <i></i> Ready
                </span>

              </div>


              <div className="speech-area">

                <span className="quote">
                  “
                </span>

                <p>
                  Your spoken words will appear here...
                </p>

              </div>


              <button
                className={`listen-button ${isListening ? 'active' : ''}`}
                onClick={() => setIsListening(!isListening)}
              >

                🎙
                {isListening
                  ? ' Stop listening'
                  : ' Start speaking'}

              </button>

            </div>


            <div className="translation-arrow">
              →
            </div>


            {/* ASL output */}

            <div className="output-panel">

              <div className="panel-top">

                <span>
                  AMERICAN SIGN LANGUAGE
                </span>

                <span className="isl-badge">
                  ASL
                </span>

              </div>


              <div className="video-placeholder">

                <div className="video-sign">
                  🤟
                </div>

                <button className="play-button">
                  ▶
                </button>

              </div>


              <div className="sign-word">
                YOUR SIGN WILL APPEAR HERE
              </div>

            </div>

          </div>

        </section>


        {/* HOW IT WORKS */}

        <section className="features-section">

          <div className="section-heading">

            <div className="tag">
              HOW IT WORKS
            </div>

            <h2>
              Simple. Fast. Accessible.
            </h2>

          </div>


          <div className="features-grid">

            <div className="feature-card">

              <div className="feature-number">
                01
              </div>

              <div className="feature-icon">
                🎙️
              </div>

              <h3>
                Speak
              </h3>

              <p>
                Speak naturally into your microphone. Your voice
                is captured and converted into text.
              </p>

            </div>


            <div className="feature-card">

              <div className="feature-number">
                02
              </div>

              <div className="feature-icon">
                ✦
              </div>

              <h3>
                Translate
              </h3>

              <p>
                The system processes your words and maps them
                to the corresponding American Sign Language signs.
              </p>

            </div>


            <div className="feature-card">

              <div className="feature-number">
                03
              </div>

              <div className="feature-icon">
                🤟
              </div>

              <h3>
                See the Sign
              </h3>

              <p>
                Watch the corresponding ASL sign demonstrations
                displayed clearly on your screen.
              </p>

            </div>

          </div>

        </section>


        {/* ABOUT */}

        <section className="about-section" id="about">

          <div className="about-content">

            <div className="tag">
              ABOUT SIGNBRIDGE
            </div>

            <h2>
              Technology that
              <br />
              <span>connects people.</span>
            </h2>

            <p>
              SignBridge is a speech-to-sign language platform
              designed to make everyday communication more
              accessible.
            </p>

            <p>
              The system takes spoken language, converts it into
              text, processes the sentence, and presents the
              corresponding American Sign Language signs through
              visual demonstrations.
            </p>

          </div>


          <div className="about-card">

            <div className="about-card-icon">
              🤝
            </div>

            <h3>
              Our Goal
            </h3>

            <p>
              To reduce communication barriers and create a
              more inclusive environment through technology.
            </p>

          </div>

        </section>


        {/* FINAL CTA */}

        <section className="cta-section">

          <div className="cta-content">

            <div className="tag">
              COMMUNICATION FOR EVERYONE
            </div>

            <h2>
              Ready to get started?
            </h2>

            <p>
              Speak your message and let SignBridge turn your
              words into American Sign Language.
            </p>

            <a
              href="#get-started"
              className="primary-button"
            >
              Start Translating <span>→</span>
            </a>

          </div>

        </section>

      </main>


      {/* FOOTER */}

      <footer>

        <div className="brand">

          <div className="brand-icon">
            🤟
          </div>

          <span>
            SignBridge
          </span>

        </div>

        <p>
          Bridging communication through American Sign Language.
        </p>

        <span className="copyright">
          © 2026 SignBridge
        </span>

      </footer>

    </div>
  )
}

export default App