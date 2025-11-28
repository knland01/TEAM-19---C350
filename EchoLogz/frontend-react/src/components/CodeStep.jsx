// CodeStep.jsx
import {useState} from "react";

export function CodeStep({ email, errors, loading, handleCodeSubmit, goBack }) {
    const [verificationCode, setVerificationCode] = useState('');
    return (
        <div className="reset-form">
            <h2>Enter Verification Code</h2>
            <p className="muted">
                We've sent a 6-digit code to <strong>{email}</strong>
            </p>

            <div className="form-group">
                <label htmlFor="code">Verification Code</label>
                <input
                    id="code"
                    type="text"
                    value={verificationCode}
                    onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                    placeholder="000000"
                    maxLength="6"
                    className={`code-input ${errors.code ? 'error' : ''}`}
                />
                {errors.code && <div className="error-message">{errors.code}</div>}
            </div>

            <button
                className="btn primary full-width"
                onClick={handleCodeSubmit}
                disabled={loading}
            >
                {loading ? 'Verifying...' : 'Verify Code'}
            </button>

            <button
                className="btn secondary full-width"
                onClick={goBack}
                style={{ marginTop: '12px' }}
            >
                Back to Sign Up
            </button>
        </div>
    );
}
