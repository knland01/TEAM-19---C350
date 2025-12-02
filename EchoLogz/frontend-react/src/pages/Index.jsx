import { useState, useEffect } from "react";
import Navbar from "../components/Navbar.jsx";

// Placeholder component
function Placeholder({ label }) {
  return (
    <div style={{ opacity: 0.9 }} className="muted">
      {label}
    </div>
  );
}

// Main Index component
export default function Index({
  signedIn,
  user,
  onLogout,
  active,
  connectSpotify,
}) {
  // Session state
  const [sessionCode, setSessionCode] = useState("");
  const [joined, setJoined] = useState(false);

  // Match state
  const [loading, setLoading] = useState(false);
  const [matchResult, setMatchResult] = useState(null);

  // Music state
  const [playlistUrl, setPlaylistUrl] = useState("");
  const [oauthConnected, setOauthConnected] = useState(false);

  // Base compatibility (fallback if no match yet)
const baseCompatibility = 78;
const compatibility = matchResult
    ? Math.round(matchResult.score * 100)
    : baseCompatibility;

  const mockIdentityA = {
    name: "You",
    features: ["Indie", "Acoustic", "Low Energy", "Warm Keys"],
  };
  const mockIdentityB = {
    name: "Match",
    features: ["Alt Rock", "High Energy", "Electronic", "Danceable"],
  };

  const API_BASE =
    import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

  const submitPlaylist = () => {
    if (!playlistUrl) {
      alert("[Submit Playlist Placeholder]");
      return;
    }
    alert(`Submitted playlist: ${playlistUrl}`);
  };

  // -----------------------------
  // NEW: Find a Match handler
  // -----------------------------
  const handleFindMatch = async () => {
    setLoading(true);
    setMatchResult(null);

    try {
      const token = localStorage.getItem("access_token");

      const resp = await fetch(`${API_BASE}/match/random`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await resp.json();

      if (!resp.ok) {
        throw new Error(data.detail || "Match generation failed.");
      }

      setMatchResult(data);
    } catch (err) {
      console.error("Error finding match:", err);
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------
  // Existing: check Spotify status
  // -----------------------------
  useEffect(() => {
    // only try if logged in and we have a token
    if (!signedIn || !user?.accessToken) return;

    async function fetchSpotifyStatus() {
      try {
        const resp = await fetch(`${API_BASE}/auth/spotify/status`, {
          headers: {
            Authorization: `Bearer ${user.accessToken}`,
            "Content-Type": "application/json",
          },
        });

        if (!resp.ok) {
          console.error("Failed to get Spotify status");
          return;
        }

        const data = await resp.json();
        setOauthConnected(data.connected);
      } catch (err) {
        console.error("Error checking Spotify status:", err);
      }
    }

    fetchSpotifyStatus();
  }, [signedIn, user, API_BASE]);

  return (
    <>
      <Navbar
        signedIn={signedIn}
        user={user}
        active={active}
        onLogout={onLogout}
      />

      <div className="app">
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

              {/* NEW: Find a Match button */}
              <button
                className="primary-btn identity-btn"
                onClick={handleFindMatch}
                disabled={loading}
                style={{ marginBottom: "1rem" }}
              >
                {loading ? "Finding Match…" : "Find a Match"}
              </button>

              <div className="session-active">
                <input
                  type="text"
                  value={sessionCode}
                  onChange={(e) => setSessionCode(e.target.value)}
                  readOnly={joined}
                  className="session-code"
                  placeholder="Session code"
                />

                {joined ? (
                  <button
                    className="btn secondary small"
                    onClick={() => {
                      setJoined(false);
                      setSessionCode("");
                    }}
                  >
                    Leave Session
                  </button>
                ) : (
                  <div style={{ display: "flex", gap: 8 }}>
                    <button
                      className="btn small"
                      onClick={() => {
                        const code = Math.random()
                          .toString(36)
                          .slice(2, 8)
                          .toUpperCase();
                        setSessionCode(code);
                        setJoined(true);
                      }}
                    >
                      New
                    </button>

                    <button
                      className="btn secondary small"
                      onClick={() => {
                        if (!sessionCode) {
                          alert("Enter a session code first.");
                          return;
                        }
                        setJoined(true);
                      }}
                    >
                      Join
                    </button>
                  </div>
                )}
              </div>

              <div className="session-note">
                {joined
                  ? "You are in a session. Share the code above."
                  : "Enter a session code or create a new session."}
              </div>
            </div>

            <hr className="divider" />

            <div className="music-panel">
              <div
                className={`oauth-btn ${
                  oauthConnected ? "connected" : ""
                }`}
                onClick={connectSpotify}
              >
                <img
                  src="https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Primary_Logo_RGB_White.png"
                  alt="Spotify"
                  className="spotify-logo"
                />
                {oauthConnected
                  ? "Spotify Connected"
                  : "Connect with Spotify"}
              </div>

              <div className="or-separator">— OR —</div>

              <div className="playlist-input">
                <input
                  type="text"
                  placeholder="Paste public Spotify playlist URL"
                  value={playlistUrl}
                  onChange={(e) => setPlaylistUrl(e.target.value)}
                  disabled={oauthConnected}
                />
                <button
                  className="btn small"
                  onClick={submitPlaylist}
                  disabled={oauthConnected}
                >
                  Submit
                </button>
              </div>

              {oauthConnected && (
                <div className="spotify-note">
                  Spotify account connected. Playlist URL input disabled.
                </div>
              )}
            </div>
          </section>
        </aside>

        <main className="right-grid">
          <div className="panel summary" style={{ alignItems: "center" }}>
            <div style={{ flex: 1 }}>
              <h2 style={{ margin: "0 0 6px 0" }}>Your Compatibility</h2>
              {matchResult && (
                <div className="muted">
                  Random match score: {compatibility}%
                </div>
              )}
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
              <div className="heatmap">COMPATIBILITY HEATMAP</div>
            </div>
          </div>

          <div
            className="panel"
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 12,
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <h3 style={{ margin: 0 }}>Recommendations</h3>
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
                  <Placeholder label="Play / Add" />
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </>
  );
}