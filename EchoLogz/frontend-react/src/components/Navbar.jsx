export default function Navbar({signedIn=false, username='', active=''}) {
    return (
    <nav className="navbar">
        <div className="navbar-left">
        <a href="index.html" style={{textDecoration: 'none', color: 'inherit'}}>
            <header className="site-brand">
                <div className="logo">EL</div>
                <div>
                <h1>EchoLogz</h1>
                <p className="lead">{signedIn ? 'Your Music. Your Match.' : 'Your music. Your match.'}</p>
                </div>
            </header>
        </a>
        </div>
        <div className="navbar-right">
        {signedIn ? (
            <>
            <a href="/index" className={`nav-link ${active==="Dashboard"?"active":""}`}>Dashboard</a>
            <a href="history_mockup.html" className={`nav-link ${active==="Saved"?"active":""}`}>Saved</a>
            <a href="account.html" className={`nav-link ${active==="Account"?"active":""}`}>Account</a>
            <a href="/sign_in" className="nav-link signup">Log Out</a>
            </>
        ) : (
            <>
            <a href="/sign_in" className="nav-link">Log In</a>
            <a href="/sign_up" className="nav-link signup">Sign Up</a>
            </>
        )}
        </div>
    </nav>
    );
}
