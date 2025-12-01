import { useState } from 'react';
import { Routes, Route} from 'react-router-dom';
import SignUp from './pages/SignUp';
import Navbar from './components/Navbar.jsx';
import './App.css';
import Index from "./pages/Index.jsx";
import Login from "./pages/Login.jsx";
import Home from "./pages/Home.jsx";

function Placeholder({ label }) {
    return <div style={{ opacity: 0.9 }} className="muted">{label}</div>;
}

function EchoLogzMockup() {
    const [sessionCode, setSessionCode] = useState('');
    const [playlistUrl, setPlaylistUrl] = useState('');
    const [joined, setJoined] = useState(false);
    const [oauthConnected, setOauthConnected] = useState(false);
    const [signedIn, setSignedIn] = useState(false);
    const username = "Duncan";

    const compatibility = 78;
    const mockIdentityA = { name:'You', features:[ 'Indie', 'Acoustic', 'Low Energy', 'Warm Keys' ]};
    const mockIdentityB = { name:'Match', features:['Alt Rock','High Energy','Electronic','Danceable']};

    function createSession(){
        // Generate a code and store it in state so JSX can read it.
        const code = Math.random().toString(36).slice(2,8).toUpperCase();
        setSessionCode(code);
    }

    function joinSession(){
        if(!sessionCode){ alert('Create or enter a session code first.'); return; }
        setJoined(true);
    }

    function connectSpotify(){
        // window.location.href="/auth/spotify/login"; <-- removed from original
        setOauthConnected(true);
        alert('[Spotify OAuth Placeholder]');
    }

    function submitPlaylist(){
        if(!playlistUrl){ alert('[Submit Playlist Placeholder]'); return; }
        setJoined(true);
    }

    return (
        <div className="app-container">
            <Navbar signedIn={signedIn} username={username} />
            {/* ...rest of your JSX... */}
            {/* Keep all JSX from your EchoLogzMockup here */}
        </div>
    );
}

// REACT ROUTER:
export default function App() {
    return <>
        <Routes>
            <Route path="/" element={<Home/>} />
            <Route path="/sign_up" element={<SignUp/>} />
            <Route path="/log_in" element={<Login/>} />
            <Route path="/dashboard" element={<Index/>} />
        </Routes>
    </>;
}
