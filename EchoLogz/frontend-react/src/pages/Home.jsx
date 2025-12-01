// MODULE: pages/Home.jsx
// Public landing page that shows a read-only preview of the EchoLogz dashboard.
// All controls are disabled and annotated with instructions.
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar.jsx";
import "../pw-style.css";

// Reuse the small placeholder helper from Index
function Placeholder({ label }) {
  return <div style={{ opacity: 0.9 }} className="muted">{label}</div>;
}

export default function Home() {
  // Static example data (same as dashboard mock)
  const compatibility = 78;
  const mockIdentityA = {
    name: "You",
    features: ["Indie", "Acoustic", "Low Energy", "Warm Keys"],
  };
  const mockIdentityB = {
    name: "Match",
    features: ["Alt Rock", "High Energy", "Electronic", "Danceable"],
  };
  const navigate = useNavigate(); 
  return (
    <>
      <Navbar />
      <div className="hero-section">
          <h2 className="hero-title">Find Your Music Match.</h2>
          <div className="hero-subtitle">
              <h2>Discover who you really vibe with — friends, partners, coworkers or total strangers.</h2>
              <p>
              EchoLogz creates a musical identity for you based on your Spotify playlists
              <br />and helps you find compatible matches through shared musical tastes.
              </p>
          </div>
          <button
              className="btn primary"
              style={{ 
                  fontSize: "1.2rem", 
                  padding: "14px 32px", 
                  marginTop: "16px"
              }}
              onClick={() => navigate("/sign_up")}
          >
              Sign Up Now FREE — Start Matching
          </button>
      </div>

      <div className="app">
        {/* LEFT COLUMN: Session + Spotify preview (read-only) */}
        <aside className="panel">
          <section className="create-join">
            <div className="session-panel">
              <label
                style={{
                  fontWeight: 600,
                  marginBottom: 6,
                  display: "block",
                }}
              >
                Compare Session
              </label>

              <div className="session-active">
                <input
                  type="text"
                  value="ABCD12"
                  readOnly
                  className="session-code"
                  placeholder="Session code"
                />

                <div style={{ display: "flex", gap: 8 }}>
                  <button className="btn small" disabled
                    style={{ pointerEvents: "none", cursor: "default", opacity: 0.7 }}>
                    New
                  </button>
                  <button className="btn secondary small" disabled
                  style={{ pointerEvents: "none", cursor: "default", opacity: 0.7 }}>
                    Join
                  </button>
                </div>
              </div>

              <div className="session-note">
                On the real dashboard, you can create or join a session using a
                unique session code to compare music with a friend.
              </div>
            </div>

            <hr className="divider" />

            <div className="music-panel">
              <div className="oauth-btn" style={{ cursor: "default", pointerEvents: "none", opacity: 0.9 }}>
                <img
                  src="https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Primary_Logo_RGB_White.png"
                  alt="Spotify"
                  className="spotify-logo"
                />
                Connect with Spotify
              </div>

              <div className="or-separator">— OR —</div>

              <div className="playlist-input">
                <input
                  type="text"
                  placeholder="Paste public Spotify playlist URL"
                  value="https://open.spotify.com/playlist/..."
                    disabled
                    style={{ cursor: "default" }}
                />
                <button className="btn small" disabled
                style={{ pointerEvents: "none", cursor: "default", opacity: 0.7 }}>
                  Submit
                </button>
              </div>

              <div className="spotify-note">
                Here, users will either connect their Spotify account or paste a
                public playlist to generate compatibility insights.
              </div>
            </div>
          </section>
        </aside>

        {/* RIGHT COLUMN: Compatibility + identity + recommendations preview */}
        <main className="right-grid">
          <div
            className="panel summary"
            style={{ alignItems: "center" }}
          >
            <div style={{ flex: 1 }}>
              <h2 style={{ margin: "0 0 6px 0" }}>Your Compatibility</h2>
              <p className="muted" style={{ fontSize: 13 }}>
                This preview shows how EchoLogz will summarize your overall
                music match score with another user.
              </p>
            </div>
            <div>
              <div
                className="score-bubble"
                style={{
                  background: `conic-gradient(var(--accent-color) 0deg, var(--accent-color) ${
                    compatibility * 3.6
                  }deg, #333 ${compatibility * 3.6}deg 360deg)`,
                }}
              >
                <span>{compatibility}%</span>
              </div>
            </div>
          </div>

          <div className="panel identity-grid">
            {[mockIdentityA, mockIdentityB].map((identity, idx) => (
              <div className="identity-card" key={idx}>
                <h3>{identity.name}</h3>
                <div className="muted">
                  Musical identity (aggregated features sample)
                </div>
                <div style={{ height: 10 }} />
                <div className="feature-list">
                  {identity.features.map((f, i) => (
                    <div className="chip" key={i}>
                      {f}
                    </div>
                  ))}
                </div>
              </div>
            ))}

            <div style={{ gridColumn: "1 / 3" }}>
              <div className="heatmap">
                COMPATIBILITY HEATMAP PREVIEW
                <div className="muted" style={{ fontSize: 13, marginTop: 4 }}>
                  On your actual dashboard, this section will visualize how your tastes
                  align across genres, moods, and energy levels.
                </div>
              </div>
            </div>
          </div>

          <div
            className="panel"
            style={{ display: "flex", flexDirection: "column", gap: 12 }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <h3 style={{ margin: 0 }}>Recommendations</h3>
              <span className="muted" style={{ fontSize: 13 }}>
                Example matches based on your shared taste.
              </span>
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr 1fr",
                gap: 12,
              }}
            >
              {[1, 2, 3].map((n) => (
                <div
                  className="identity-card"
                  style={{ padding: 10 }}
                  key={n}
                >
                  <div style={{ fontWeight: 700 }}>
                    #{n} — Example Song
                  </div>
                  <div className="muted" style={{ fontSize: 13 }}>
                    Artist • Album
                  </div>
                  <Placeholder label="In the real app, you'll be able to play or add this track." />
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </>
  );
}