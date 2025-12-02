import { useState } from "react";
import Navbar from "../components/Navbar.jsx";
import "../style_history.css";

export default function MusicID({
  signedIn,
  user,
  onLogout,
  active,
  connectSpotify,
}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [profile, setProfile] = useState(null);

  const handleGenerateClick = async () => {
    if (!user?.id) {
      setError("You must be logged in to generate your identity.");
      return;
    }

    setLoading(true);
    setError("");
    setProfile(null);

    try {
      const token = localStorage.getItem("access_token");

      const resp = await fetch(
        `http://localhost:8000/match/identity/${user.id}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await resp.json();

      if (!resp.ok) {
        throw new Error(data.detail || "Failed to build identity.");
      }

      // { user_id, raw, scaled, labels }
      setProfile(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // simple inline styles to mimic the dark card / table look
  const cardStyle = {
    marginTop: "2rem",
    background: "rgba(10, 5, 25, 0.95)",
    borderRadius: "16px",
    padding: "1.5rem 2rem",
    boxShadow: "0 12px 30px rgba(0, 0, 0, 0.4)",
  };

  const tableWrapperStyle = {
    marginTop: "1.25rem",
    overflowX: "auto",
  };

  const tableStyle = {
    width: "100%",
    borderCollapse: "collapse",
    fontSize: "0.9rem",
  };

  const thTdBase = {
    padding: "0.5rem 0.75rem",
    textAlign: "left",
    borderBottom: "1px solid rgba(255,255,255,0.08)",
  };

  const pillStyle = {
    display: "inline-block",
    padding: "0.1rem 0.6rem",
    borderRadius: "999px",
    fontSize: "0.8rem",
    background: "rgba(137, 97, 255, 0.18)",
    border: "1px solid rgba(137, 97, 255, 0.6)",
  };

  return (
    <>
      <Navbar
        signedIn={signedIn}
        user={user}
        active={active}
        onLogout={onLogout}
      />

      <main className="page-container">
        <h1>Musical Identity</h1>

        <p className="muted">
          Use your connected Spotify account to generate an aggregated profile
          of your listening habits.
        </p>

        <button
          className="primary-btn identity-btn"
          onClick={handleGenerateClick}
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate My Musical Identity"}
        </button>

        {error && (
          <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>
        )}

        {/* ---------------------------------------------------------- */}
        {/*                        PROFILE ID OUTPUT                   */}
        {/* ---------------------------------------------------------- */}

        {profile && (
          <section className="identity-results" style={cardStyle}>
            <h2>Your Identity Profile</h2>

            <div style={tableWrapperStyle}>
              <table style={tableStyle}>
                <thead>
                  <tr>
                    <th style={{ ...thTdBase, fontWeight: 500 }}>
                      Feature
                    </th>
                    <th style={{ ...thTdBase, fontWeight: 500 }}>
                      Raw
                    </th>
                    <th style={{ ...thTdBase, fontWeight: 500 }}>
                      Scaled
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {profile.labels.map((label, idx) => (
                    <tr
                      key={label}
                      style={{
                        background:
                          idx % 2 === 0
                            ? "rgba(255,255,255,0.02)"
                            : "rgba(255,255,255,0.04)",
                      }}
                    >
                      <td style={thTdBase}>
                        {label}
                      </td>
                      <td style={thTdBase}>
                        {profile.raw &&
                          profile.raw[label] !== undefined &&
                          Number(profile.raw[label]).toFixed(4)}
                      </td>
                      <td style={thTdBase}>
                        <span style={pillStyle}>
                          {profile.scaled &&
                            profile.scaled[idx] !== undefined &&
                            Number(profile.scaled[idx]).toFixed(3)}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {!profile && !loading && !error && (
          <section
            className="identity-results"
            style={{ marginTop: "2rem" }}
          >
            <p className="muted">
              Your musical identity will appear here once generated.
            </p>
          </section>
        )}
      </main>
    </>
  );
}