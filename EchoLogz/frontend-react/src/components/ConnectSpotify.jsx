/**
 * MODULE: components/ConnectSpotify.jsx
 * 
 * Handles the Spotify OAuth connection UI after the user is authenticated.
 * 
 * Provides a button or link that starts the Spotify OAuth process and displays
 * state related to connecting the user's Spotify account. Assumes the user
 * is already logged in and has a valid Echologz account.
 */



/*// // src/components/SpotifyLinkStep.jsx
// import React from "react";

// const API_BASE_URL =
//   import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// export function SpotifyLinkStep({ goNext }) {

//   const handleConnectClick = () => {
//     window.location.href = `${API_BASE_URL}/auth/spotify/login`;
//   };

//   const handleSkip = () => {
//     goNext();  // Moves to the next step in your SignUp.jsx
//   };

//   return (
//     <div className="reset-form">
//         <h2>Connect Your Spotify Account</h2>

//         <p className="muted">
//         You can link your Spotify account now, or skip this and link it later
//         in your EchoLogz dashboard.
//         </p>

//         <button
//             className="btn primary full-width" 
//             onClick={handleConnectClick}
//         >
//             Connect with Spotify
//         </button>
 
//         <button
//             className="btn-secondary full-width"
//             onClick={handleSkip} style={{ marginTop: "15px" }}
//         >
//             Skip
//         </button>
//     </div>
//   );
// }}


     /* Spotify OAuth Styled Button
        <div className="music-panel">
            <div className="oauth-btn" 
                onClick={handleConnectClick}>
            <img
                src="https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Primary_Logo_RGB_White.png"
                className="spotify-logo"
                alt="Spotify"
            />
            Connect with Spotify
            </div>
        </div> */