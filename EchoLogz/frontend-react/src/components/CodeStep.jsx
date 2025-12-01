/**
 * MODULE: components/CodeStep.jsx
 * Step 2 of the signup flow.
 * 
 * Displays the email verification instructions and provides UI for checking whether
 * the user has clicked the verification link. Invokes onVerifyClick() to trigger the
 * backend verification status check. Errors and success states are controlled by
 * the parent SignUp.jsx.
 */

import {useState} from "react";
import React from "react";

export function CodeStep({ email, verifyExpiresIn, errors, loading, onVerifyClick, goBack, onResendClick, verifySuccess, }) {
  return (
    <div className="reset-form">
        <h2>Verify Your Email</h2>
        <p className="muted">
            We've sent a verification link to <strong>{email}</strong>.<br />
            DEV: Clickable link in <strong>TERMINAL</strong> until email system set up proper.<br />
            After you've clicked the link, press the button below to continue.
        </p>
        {verifyExpiresIn !== null && (
            <p className="muted" style={{ marginTop: "4px" }}>
                The verification link expires in <strong>{verifyExpiresIn} minutes</strong>.
            </p>
            )}

        <button
            className="btn secondary full-width"
            style={{ marginTop: "12px" }}
            onClick={onResendClick}
            type="button"
        >
            Resend verification link
        </button>

        {/* Error from backend (invalid / expired token, etc.) */}
        {errors.code && (
            <div className="error-message">{errors.code}</div>
        )}

        {verifySuccess && !errors.code && (
            <div className="success-message" style={{ marginTop: "12px" }}>
            You're all set. You can now Log In to EchoLogz.
            </div>
        )}

        <button
            className="btn primary full-width"
            onClick={onVerifyClick}
            disabled={loading || verifySuccess}
        >
            {loading
                ? "Verifying..." : verifySuccess 
                ? "Email verified!" : "I've verified my email"}
        </button>



        <button
            className="btn secondary full-width"
            onClick={goBack}
            style={{ marginTop: "12px" }}
        >
            Back to Sign Up
        </button>
    </div>
  );
}









/* ----------------------------- CODE GRAVEYARD ------------------------------------------------------
// NOTE: Back-end supports JWT token authorization = easier implementation than 6 digit code.

// export function CodeStep({ email, errors, loading, handleCodeSubmit, goBack }) {
//     const [verificationCode, setVerificationCode] = useState('');
//     return (
//         <div className="reset-form">
//             <h2>Enter Verification Code</h2>
//             <p className="muted">
//                 We've sent a 6-digit code to <strong>{email}</strong>
//             </p>

//             <div className="form-group">
//                 <label htmlFor="code">Verification Code</label>
//                 <input
//                     id="code"
//                     type="text"
//                     value={verificationCode}
//                     onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
//                     placeholder="000000"
//                     maxLength="6"
//                     className={`code-input ${errors.code ? 'error' : ''}`}
//                 />
//                 {errors.code && <div className="error-message">{errors.code}</div>}
//             </div>

//             <button
//                 className="btn primary full-width"
//                 onClick={() => handleCodeSubmit(verificationCode)}
//                 disabled={loading}
//             >
//                 {loading ? 'Verifying...' : 'Verify Code'}
//             </button>

//             <button
//                 className="btn secondary full-width"
//                 onClick={goBack}
//                 style={{ marginTop: '12px' }}
//             >
//                 Back to Sign Up
//             </button>
//         </div>
//     );
// } */
