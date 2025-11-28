// src/SignUp.jsx
import { useState } from 'react';
import Navbar from '../components/Navbar.jsx';
// import { validateEmail, validatePassword, passwordsMatch } from '../utils';
import {StepIndicator} from "../components/StepIndicator.jsx";
import {AccountStep} from "../components/AccountStep.jsx";
import {CodeStep} from "../components/CodeStep.jsx";
import '../pw-style.css';

export default function SignUp() {
    const [step, setStep] = useState(1);     // Step 1: Account info, Step 2: Verification code
    const [loading, setLoading] = useState(false);

    return (
        <div className="app-container">
            <Navbar />

            <div className="reset-container">
                <div className="reset-panel panel">

                    <StepIndicator step={step} />

                    {step === 1 ? (
                        <AccountStep
                            loading={loading}
                            setLoading={setLoading}
                            setStep={setStep}
                        />
                    ) : (
                        <CodeStep />
                    )}
                </div>
            </div>
        </div>
    );
}
