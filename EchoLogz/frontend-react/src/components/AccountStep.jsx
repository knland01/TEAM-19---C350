import {useState} from "react";
import {passwordsMatch, validateEmail, validatePassword} from "../utils.js";

export function AccountStep({loading}) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [errors, setErrors] = useState({});


    function handleSignUpSubmit() {
        setErrors({});
        const newErrors = {};

        if (!email) newErrors.email = 'Email is required';
        else if (!validateEmail(email)) newErrors.email = 'Invalid email address';

        if (!password) newErrors.password = 'Password is required';
        else if (!validatePassword(password)) newErrors.password = 'Password must be at least 8 characters';

        if (!confirmPassword) newErrors.confirmPassword = 'Please confirm your password';
        else if (!passwordsMatch(password, confirmPassword)) newErrors.confirmPassword = 'Passwords do not match';

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }

        setLoading(true);
        // Simulate API call
        setTimeout(() => {
            setLoading(false);
            setStep(2);
        }, 1200);
    }

    return (
        <div className="reset-form">
            <h2>Create Your Account</h2>
            <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email address"
                    className={errors.email ? 'error' : ''}
                />
                {errors.email && <div className="error-message">{errors.email}</div>}
            </div>
            <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Create a password"
                    autoComplete="new-password"
                    className={errors.password ? 'error' : ''}
                />
                {errors.password && <div className="error-message">{errors.password}</div>}
            </div>
            <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password</label>
                <input
                    id="confirmPassword"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Confirm password"
                    autoComplete="new-password"
                    className={errors.confirmPassword ? 'error' : ''}
                />
                {errors.confirmPassword && <div className="error-message">{errors.confirmPassword}</div>}
            </div>

            <button
                className="btn primary full-width"
                onClick={handleSignUpSubmit}
                disabled={loading}
            >
                {loading ? 'Creating Account...' : 'Sign Up'}
            </button>
        </div>
    );
}
