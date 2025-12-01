// src/pages/PasswordResetPage.jsx
import React, { useState } from "react";
import Navbar from "../components/Navbar.jsx";

import "../style_history.css";
import "../pw-style.css";

// Adjust this import path to wherever your helpers live
import {
  validateEmail,
  validatePassword,
  passwordsMatch
} from "../utils.js"; // <-- fix path as needed

export default function PasswordResetPage(){
    const [email, setEmail] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [resetCode, setResetCode] = useState('');
    const [step, setStep] = useState(1); // 1: Email, 2: Code, 3: New Password, 4: Success
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

function handleEmailSubmit() {
    setErrors({});
    if (!email) {
    setErrors({email: 'Email is required'});
    return;
    }
    if (!validateEmail(email)) {
    setErrors({email: 'Please enter a valid email address'});
    return;
    }
    
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
    setLoading(false);
    setStep(2);
    }, 1000);
}

function handleCodeSubmit() {
    setErrors({});
    if (!resetCode) {
    setErrors({code: 'Verification code is required'});
    return;
    }
    if (resetCode.length !== 6) {
    setErrors({code: 'Code must be 6 digits'});
    return;
    }
    
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
    setLoading(false);
    setStep(3);
    }, 1000);
}

function handlePasswordSubmit() {
    setErrors({});
    const newErrors = {};

    if (!newPassword) {
    newErrors.newPassword = 'Password is required';
    } else if (!validatePassword(newPassword)) {
    newErrors.newPassword = 'Password must be at least 8 characters, contain letters and numbers, and have no spaces';
    }

    if (!confirmPassword) {
    newErrors.confirmPassword = 'Please confirm your password';
    } else if (!passwordsMatch(newPassword, confirmPassword)) {
    newErrors.confirmPassword = 'Passwords do not match';
    }

    if (Object.keys(newErrors).length > 0) {
    setErrors(newErrors);
    return;
    }

    setLoading(true);
    // Simulate API call
    setTimeout(() => {
    setLoading(false);
    setStep(4);
    }, 1000);
}



return (
    <div className="app-container">
    <Navbar />

    <div className="reset-container">
        <div className="reset-panel panel">
        {/* Step Indicator */}
        <div className="step-indicator">
            <div className={`step ${step >= 1 ? 'active' : ''} ${step > 1 ? 'completed' : ''}`}>
            <div className="step-number">1</div>
            <div className="step-label">Email</div>
            </div>
            <div className="step-line"></div>
            <div className={`step ${step >= 2 ? 'active' : ''} ${step > 2 ? 'completed' : ''}`}>
            <div className="step-number">2</div>
            <div className="step-label">Verify</div>
            </div>
            <div className="step-line"></div>
            <div className={`step ${step >= 3 ? 'active' : ''} ${step > 3 ? 'completed' : ''}`}>
            <div className="step-number">3</div>
            <div className="step-label">Reset</div>
            </div>
        </div>
        
        {/* Step 1: Email */}
        {step === 1 && (
            <div className="reset-form">
            <h2>Reset Your Password</h2>
            <p className="muted">Enter your email address and we'll send you a verification code.</p>
            
            <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input
                id="email"
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="Enter your email address"
                className={errors.email ? 'error' : ''}
                />
                {errors.email && <div className="error-message">{errors.email}</div>}
            </div>

            <button 
                className="btn primary full-width" 
                onClick={handleEmailSubmit}
                disabled={loading}
            >
                {loading ? 'Sending...' : 'Send Verification Code'}
            </button>
            </div>
        )}

        {/* Step 2: Code Verification */}
        {step === 2 && (
            <div className="reset-form">
            <h2>Enter Verification Code</h2>
            <p className="muted">We've sent a 6-digit code to <strong>{email}</strong></p>
            
            <div className="form-group">
                <label htmlFor="code">Verification Code</label>
                <input
                id="code"
                type="text"
                value={resetCode}
                onChange={e => setResetCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
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
                onClick={() => setStep(1)}
                style={{marginTop: '12px'}}
            >
                Back to Email
            </button>
            </div>
        )}

        {/* Step 3: New Password */}
        {step === 3 && (
            <div className="reset-form">
            <h2>Create New Password</h2>
            <p className="muted">Choose a strong password for your account.</p>
            
            <div className="form-group">
                <label htmlFor="newPassword">New Password</label>
                <input
                id="newPassword"
                type="password"
                value={newPassword}
                onChange={e => setNewPassword(e.target.value)}
                placeholder="Enter new password"
                className={errors.newPassword ? 'error' : ''}
                />
                {errors.newPassword && <div className="error-message">{errors.newPassword}</div>}
            </div>

            <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password</label>
                <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
                placeholder="Confirm new password"
                className={errors.confirmPassword ? 'error' : ''}
                />
                {errors.confirmPassword && <div className="error-message">{errors.confirmPassword}</div>}
            </div>

            <button 
                className="btn primary full-width" 
                onClick={handlePasswordSubmit}
                disabled={loading}
            >
                {loading ? 'Updating...' : 'Update Password'}
            </button>

            <button 
                className="btn secondary full-width" 
                onClick={() => setStep(2)}
                style={{marginTop: '12px'}}
            >
                Back to Verification
            </button>
            </div>
        )}

        {/* Step 4: Success */}
        {step === 4 && (
            <div className="reset-form success">
            <div className="success-icon">✓</div>
            <h2>Password Reset Successful!</h2>
            <p className="muted">Your password has been successfully updated. You can now sign in with your new password.</p>
            
            <button 
                className="btn primary full-width"
                onClick={() => window.location.href = 'sign_in.html'}
            >
                Sign In to Your Account
            </button>
            </div>
        )}
        </div>
    </div>
    </div>
)
}

