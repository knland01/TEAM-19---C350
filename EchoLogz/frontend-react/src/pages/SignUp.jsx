// src/SignUp.jsx
import { useState } from 'react';
import Navbar from '../components/Navbar.jsx';
import { validateEmail, validatePassword, passwordsMatch } from '../utils';
import {StepIndicator} from "../components/StepIndicator.jsx";
import {AccountStep} from "../components/AccountStep.jsx";
import {CodeStep} from "../components/CodeStep.jsx";
import '../pw-style.css';

export default function SignUp() {
    const [step, setStep] = useState(1); // 1: Info, 2: Code
    const [loading, setLoading] = useState(false);

    // Main render
    return (
        <div className="app-container">
            <Navbar />
            <div className="reset-container">
                <div className="reset-panel panel">
                    <StepIndicator />
                    {step === 1 ? <AccountStep loading={loading} /> : <CodeStep />}
                </div>
            </div>
        </div>
    );
}
