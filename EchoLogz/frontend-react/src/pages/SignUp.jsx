/**
 * MODULE: pages/SignUp.jsx
 * 
 * Main signup page controller.
 * 
 * Manages the multi-step signup pipeline, including step navigation, loading state,
 * verification state, success states, and error handling. Renders AccountStep for
 * creating the account and CodeStep for email verification. Coordinates backend calls
 * and determines when the user advances to the next step.
 */


import { useState } from 'react'; 
// ... react stores state in variable (ex: step, loading) | changes state with function (ex: setStep, setLoading) 
import Navbar from '../components/Navbar.jsx';
// import { validateEmail, validatePassword, passwordsMatch } from '../utils';
import {StepIndicator} from "../components/StepIndicator.jsx";
import {AccountStep} from "../components/AccountStep.jsx";
import {CodeStep} from "../components/CodeStep.jsx";
// import {SpotifyLinkStep} from '../components/SpotifyLinkStep.jsx';
import '../pw-style.css';

export default function SignUp() {
    
    const [step, setStep] = useState(1);  
    // ... setStep useState(1)--> STEP 1: Account info
    // ... setStep useState(2) ---> STEP 2: Verify email
    const [loading, setLoading] = useState(false); // loading useState(true) = talking to backend
    const [signupEmail, setSignupEmail] = useState(""); // email from step 1 → shown in step 2
    const [verifyToken, setVerifyToken] = useState("");  // JWT returned from /signup
    const [codeErrors, setCodeErrors] = useState({}); // errors shown in CodeStep
    const [verifyExpiresIn, setVerifyExpiresIn] = useState(null); // show expire time to user
    const [verifySuccess, setVerifySuccess] = useState(false);


    function handleSignupSuccess({ email, verifyToken, verifyExpiresIn }) {
        setSignupEmail(email);
        setVerifyToken(verifyToken);
        setVerifyExpiresIn(verifyExpiresIn);
        setCodeErrors({});
        setVerifySuccess(false);
        setStep(2);
    }

    // Step 2: verify email using token
    async function handleVerifyClick() {
        if (!signupEmail) {
            setCodeErrors({ code: "Missing email. Please sign up again." });
            return;
        }

        setLoading(true);
        setCodeErrors({});
        setVerifySuccess(false);
        try {
            const resp = await fetch(`http://localhost:8000/auth/verify-status?email=${encodeURIComponent(signupEmail)}`);

            if (!resp.ok) {
            const data = await resp.json().catch(() => null);
            const msg = data?.detail || "Could not check verification status.";
            setCodeErrors({ code: msg });
            return;
            }

            const data = await resp.json();
            console.log("verify-status:", data);

            if (!data.is_verified) {
                setCodeErrors({
                    code:
                    "Please verify your email by clicking the link we sent, " +
                    "then click this button again.",
                });
                return;
            }
            setVerifySuccess(true);
            // TODO: REDIRECT TO LOGIN PAGE HERE
                
            // setStep(3); // STEP 3 ---> moved to dashboard
        } catch (err) {
            console.error("Verify error:", err);
            setCodeErrors({ code: "Network error. Please try again." });
        } finally {
            setLoading(false);
        }
    }
    function handleResendClick() {
        setCodeErrors({
            code: "TODO: Code Assignment (Resend v.link not implemented yet)"
        });
    }


    return (
    <div className="app-container">
        <Navbar />

        <div className="reset-container">
            <div className="reset-panel panel">
                <StepIndicator step={step} />

                {step === 1 && (
                <AccountStep
                    loading={loading}
                    setLoading={setLoading}
                    setStep={setStep}
                    onSignupSuccess={handleSignupSuccess}
                />
                )}

                {step === 2 && (
                <CodeStep
                    email={signupEmail}
                    errors={codeErrors}
                    loading={loading}
                    onVerifyClick={handleVerifyClick}
                    verifyExpiresIn={verifyExpiresIn}
                    verifySuccess={verifySuccess}
                    goBack={() => setStep(1)}
                    onResendClick={handleResendClick}
                />
                )}

                {/* {step === 3 && ( // KL: Spotify link needs to happen AFTER Echologz user is fully logged in for simplicity
                <SpotifyLinkStep
                    loading={loading}
                    setLoading={setLoading}
                />
                )} */}
            </div>
        </div>
    </div>
  );
}
