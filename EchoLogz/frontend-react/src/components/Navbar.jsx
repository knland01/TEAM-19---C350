/**
 * MODULE: components/Navbar.jsx
 * 
 * Global navigation bar component.
 * 
 * Provides site-wide navigation links and branding. Contains UI only – no backend
 * communication and no page-level state. Reused across multiple pages.
 */

import { Link } from "react-router-dom";

export default function Navbar({signedIn=false, user='', active='', onLogout = () => {}}) {
    return (
    <nav className="navbar">
        <div className="navbar-left">
        <Link to={signedIn ? "/dashboard" : "/"} 
            style={{ textDecoration: 'none', color: 'inherit' }}
        >
            <header className="site-brand">
                <div className="logo">EL</div>
                <div>
                <h1>EchoLogz</h1>
                <p className="lead">{signedIn ? 'Your Music. Your Match.' : 'Your music. Your match.'}</p>
                </div>
            </header>
        </Link>
        </div>
        <div className="navbar-right">
        {signedIn ? (
            <>
            <Link to="/dashboard" className={`nav-link ${active==="Dashboard"?"active":""}`}>Dashboard</Link>
            <Link to="/history" className={`nav-link ${active==="Saved"?"active":""}`}>History</Link>
            <Link to="/account" className={`nav-link ${active==="Account"?"active":""}`}>Account</Link>
            {/* <Link to="/log_in" className="nav-link signup">Log Out</Link> */}
            <span className="nav-link" 
                style={{ cursor: "pointer" }} 
                onClick={onLogout}>
                Logout
            </span>
            <span className="nav-user">
                {user?.email ?? user}
            </span>
            </>
        ) : (
            <>
            <Link to="/log_in" className="nav-link">Log In</Link>
            <Link to="/sign_up" className="nav-link signup">Sign Up</Link>
            </>
        )}
        </div>
    </nav>
    );
}
