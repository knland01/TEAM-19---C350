/**
 * MODULE: pages/Login.jsx
 * 
 * Login page component.
 * 
 * Renders the login form and sends email/password credentials to /auth/login.
 * Displays backend errors and, on success, typically stores the returned access token
 * and redirects the user. Does not participate in the signup step flow.
 */

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar.jsx";
import "../pw-style.css";

export default function Login({ onLoginSuccess }) { // exportable Login React component
    // STATE VARIABLES:
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    const navigate = useNavigate(); 

    // ASYNC HANDLER:
    async function handleLoginSubmit(event) { // async function that runs when form submitted
        if (event && event.preventDefault) { // prevents full-page reload (default) when form submits 
            event.preventDefault();
        }

        setErrors({}); // clears any previous errors printed on the screen 
        const newErrors = {}; // new / empty error basket

        if (!email) newErrors.email = "Email is required";
        if (!password) newErrors.password = "Password is required";

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }

        try { // enter network call block
        setLoading(true); // so button can show "Logging in"
        const resp = await fetch("http://localhost:8000/auth/login", { // call to FastAPI backend
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: email,
                password: password,
            }),
        });

        if (!resp.ok) {
            let msg = "Login failed";
            try {
                const data = await resp.json();
                if (data.detail) {
                    msg = data.detail; 
                    // if the JSON has detail - display it as user-visible message
                    // FastAPI generates + sends JSON: {detail: custom problem defined} upon failure -- instead of pydantic shaped JSON upon success
                } 
                } catch {
                // ignore JSON parse error
                }
                setErrors((prev) => ({ ...prev, form: msg }));
                return;
        }
        const data = await resp.json(); // if resp.ok parse JSON = TokenOut {access_token, token_type}
        const userData = {
            id: data.user.id,
            email: data.user.email,
            accessToken: data.access_token,
            tokenType: data.token_type,
        };
        console.log("Login success:", data); // send dev message to console indicating success
        if (onLoginSuccess) {
            onLoginSuccess(userData); // flip signedin flag to true (in App.jsx)
        }// 
        navigate("/dashboard"); // Redirect to dashboard (Index.jsx is mapped to "/")

        // TODO: store data.access_token = JWT (in localStorage or context ?)
        // TODO: redirect to dashboard / home page
        } catch (err) { // if the fetch throws error (like: server down, no internet, CORS blocks...)
            console.error("Login error:", err); // log raw error to the browser console for debugging
            setErrors((prev) => ({
                ...prev,
                form: "Network error. Please try again.", // show generic error message to user in UI
            }));
        } finally { // finally always runs whether success/fail
            setLoading(false); // sets button back to normal
        }
    }

    return (
            <div className="app-container">
            <Navbar />

            <div className="reset-container">
                <div className="reset-panel panel">
                <h2>Log In</h2>

                {errors.form && (
                    <div className="error-message">{errors.form}</div>
                )}

                <form onSubmit={handleLoginSubmit}>
                    <div className="form-group">
                    <label htmlFor="login-email">Email Address</label>
                    <input
                        id="login-email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email address"
                        className={errors.email ? "error" : ""}
                    />
                    {errors.email && (
                        <div className="error-message">{errors.email}</div>
                    )}
                    </div>

                    <div className="form-group">
                    <label htmlFor="login-password">Password</label>
                    <input
                        id="login-password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        autoComplete="current-password"
                        className={errors.password ? "error" : ""}
                    />
                    {errors.password && (
                        <div className="error-message">
                        {errors.password}
                        </div>
                    )}
                    </div>

                    <button
                    type="submit"
                    className="btn primary full-width"
                    disabled={loading}
                    >
                    {loading ? "Logging In..." : "Log In"}
                    </button>
                </form>
                </div>
            </div>
        </div>
    );
}