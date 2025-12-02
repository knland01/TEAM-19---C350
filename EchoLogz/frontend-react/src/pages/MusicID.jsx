import { useState } from "react";
import Navbar from "../components/Navbar.jsx";


export default function MusicID({ user, active }) {
    const [loading, setLoading] = useState(false);
    const [error, setError]   = useState("");
    const [profile, setProfile] = useState(null);

    const handleGenerateClick = async () => {
        if (!user?.id) {
            setError("You must be logged in to generate your identity.");
            return;
        }
        setLoading(true);
        setError("");
        try {
            const resp = await fetch(
                `http://localhost:8000/match/identity/${user.id}`
            );
            if (!resp.ok) {
                const data = await resp.json().catch(() => ({}));
                throw new Error(data.detail || "Failed to build identity.");
            }
            const data = await resp.json();  // { raw, scaled, labels }
            setProfile(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
        console.log("Generate musical identity for:", user?.email || user?.id);
    };
    return (
    <>
    <Navbar signedIn={true} active={active} onLogout={() => {}} />
    <main className="page-container">
        <h1>Musical Identity</h1>
        <p className="muted">
        Use your connected Spotify account to generate an aggregated profile
        of your listening habits.
        </p>

        <button className="primary-btn" onClick={handleGenerateClick}>
        Generate My Musical Identity
        </button>

        {/* Placeholder for results */}
        <section className="identity-results">
        <p className="muted">
            Your musical identity will appear here once generated.
        </p>
        </section>
    </main>
    </>
);
}