// StepIndicator.jsx
// Visually displays Steps/Completion on signup screen. 

export function StepIndicator({ step }) {
    return (
        <div className="step-indicator">
            <div className={`step ${step >= 1 ? 'active' : ''} ${step > 1 ? 'completed' : ''}`}>
                <div className="step-number">1</div>
                <div className="step-label">Account</div>
            </div>

            <div className="step-line"></div>

            <div className={`step ${step >= 2 ? 'active' : ''} ${step > 2 ? 'completed' : ''}`}>
                <div className="step-number">2</div>
                <div className="step-label">Verify</div>
            </div>

            <div className="step-line"></div>
            
            <div className={`step ${step >= 3 ? 'active' : ''} ${step > 3 ? 'completed' : ''}`}>
                <div className="step-number">3</div>
                <div className="step-label">Spotify</div>
            </div>
        </div>
    );
}


