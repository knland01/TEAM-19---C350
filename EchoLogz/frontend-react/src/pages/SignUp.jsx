// src/SignUp.jsx
import { useState } from 'react'; 
// ... react stores state in variable (ex: step, loading) | changes state with function (ex: setStep, setLoading) 
import Navbar from '../components/Navbar.jsx';
// import { validateEmail, validatePassword, passwordsMatch } from '../utils';
import {StepIndicator} from "../components/StepIndicator.jsx";
import {AccountStep} from "../components/AccountStep.jsx";
import {CodeStep} from "../components/CodeStep.jsx";
import '../pw-style.css';

export default function SignUp() {
    
    const [step, setStep] = useState(1);  
    // ... setStep useState(1)--> STEP 1: Account info
    // ... setStep useState(2) ---> STEP 2: Verification code
    const [loading, setLoading] = useState(false); // loading useState(true) = talking to backend

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
                        <CodeStep /> // Verification code
                    )}
                </div>
            </div>
        </div>
    );
}
