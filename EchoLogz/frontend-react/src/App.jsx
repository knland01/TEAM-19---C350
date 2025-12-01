import { useState } from 'react';
import { Routes, Route} from 'react-router-dom';
import Navbar from './components/Navbar.jsx';
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import './App.css';
import SignUp from './pages/SignUp';
import Index from "./pages/Index.jsx";
import Login from "./pages/Login.jsx";
import Home from "./pages/Home.jsx";
import Account from "./pages/Account.jsx";
import PasswordReset from "./pages/PasswordReset.jsx";
import History from "./pages/History.jsx";
import Error from "./pages/Error.jsx";


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
            <Navbar signedIn={signedIn} user={user} onLogout={handleLogout} />
            {/* ...rest of your JSX... */}
            {/* Keep all JSX from your EchoLogzMockup here */}
        </div>
    );
}


export default function App() {
    const [signedIn, setSignedIn] = useState(false);
    const [user, setUser] = useState(null);

    function handleLoginSuccess(userData) {
        setSignedIn(true);
        setUser(userData);     // ex: { email, username, id, ... }
    }

    function handleLogout() {
        setSignedIn(false);
        setUser(null);
        // TODO: clear tokens/localStorage here (if needed)
    }
    return <>
        <Routes>
            <Route path="/" element={<Home signedIn={signedIn} />} />
            <Route path="/sign_up" element={<SignUp/>} />
            <Route path="/log_in" element={<Login onLoginSuccess={handleLoginSuccess} />} />
            <Route path="/account" element={<ProtectedRoute signedIn={signedIn}><Account signedIn={signedIn} user={user} onLogout={handleLogout} active="Account"/></ProtectedRoute>} />
            <Route path="/reset_password" element={<PasswordReset />} />
            <Route path="/dashboard" element={<ProtectedRoute signedIn={signedIn}><Index signedIn={signedIn} user={user} onLogout={handleLogout} active="Dashboard" /></ProtectedRoute>} />
            <Route path="/history" element={<ProtectedRoute signedIn={signedIn}><History signedIn={signedIn} user={user} onLogout={handleLogout} active="History" /></ProtectedRoute>} />
            <Route path="/reset_password" element={<PasswordReset />} />
            <Route path="/error" element={<Error />} />
            <Route path="*" element={<Error />} />
        </Routes>
    </>;
}
