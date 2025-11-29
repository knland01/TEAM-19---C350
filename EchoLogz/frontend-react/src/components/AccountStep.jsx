import {useState} from "react";
import {passwordsMatch, validateEmail, validatePassword} from "../utils.js";

export function AccountStep({loading, setLoading, setStep}) {
    // const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [errors, setErrors] = useState({});
    const [createdUser, setCreatedUser] = useState(null); // <- backend-confirmed account


    async function handleSignUpSubmit(event) { // async allows function to use await statements
        if (event && event.preventDefault) { // so Enter / click behaves the same
            event.preventDefault(); 
        }
        setErrors({});  // wipe any old errors
        const newErrors = {}; // create new error object (basket)

        // drop errors into error basket if present...
        if (!email) newErrors.email = 'Email is required';
        else if (!validateEmail(email)) newErrors.email = 'Invalid email address';
        if (!password) newErrors.password = 'Password is required';
        else if (!validatePassword(password)) newErrors.password = 'Password must be at least 8 characters';
        if (!confirmPassword) newErrors.confirmPassword = 'Please confirm your password';
        else if (!passwordsMatch(password, confirmPassword)) newErrors.confirmPassword = 'Passwords do not match';
        
        // empty out the error basket if it has anything in it before moving on...
        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }
        try {
            setLoading(true);
            const resp = await fetch(
                "http://localhost:8000/auth/signup",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password,
                    }),
                }
            );
            if (!resp.ok) {   // only moves on if no errors
                let msg = "Sign up failed";
                try{
                    const data = await resp.json();
                    if (data.detail) {
                        msg = data.detail;
                    }
                } catch {
                    // ignore JSON parse error
                }
                setErrors((prev) => ({...prev, form: msg}));
                return;
            }
            // Turn back-end HTTP response into real JavaScript object --> to confirm sign-up success
            const user = await resp.json(); // { id, email }
            setCreatedUser(user);

            setStep(2);            

            // setStep(3); 

            } catch (err) {
                console.error("Signup error:", err);
                setErrors((prev) => ({
                ...prev,
                form: "Network error. Please try again.",
                }));
            } finally {
                setLoading(false);
            }
        }

    return (
        <div className="reset-form"> 
            <h2>Create Your Account</h2>

            {/* Backend-UserAcct made -- confirmation bubble*/}
            {createdUser && (                                    // React JSX: (&&) If LEFT return RIGHT
                <div className="success-message">
                    <strong>Account created!</strong>
                    <div>User ID: {createdUser.id}</div>
                    <div>Email: {createdUser.email}</div>
                </div>
            )}

            {/* Form-level error (API or network) */}
            {errors.form && (
                <div className="error-message">{errors.form}</div>
            )}

            <form onSubmit={handleSignUpSubmit}>
                <div className="form-group">
                    <label htmlFor="email">Email Address</label>
                    <input
                        id="email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email address"
                        className={errors.email ? "error" : ""}
                    />
                    {errors.email && (
                        <div className="error-message">
                            {errors.email}
                        </div>
                    )}
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
                        className={errors.password ? "error" : ""}
                    />
                    {errors.password && (
                        <div className="error-message">
                            {errors.password}
                        </div>
                    )}
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
                        className={errors.confirmPassword ? "error" : ""}
                    />
                    {errors.confirmPassword && (
                        <div className="error-message">
                            {errors.confirmPassword}
                        </div>
                    )}
                </div>

                <button
                    type="submit"
                    className="btn primary full-width"
                    disabled={loading}
                >
                    {loading ? "Creating Account..." : "Sign Up"}
                </button>
            </form>
        </div>
    );
}


/* ----------------------- CODE GRAVEYARD --------------------------------------------------------------------
        // setLoading(true);
        // // Simulate API call
        // setTimeout(() => {
        //     setLoading(false);
        //     setStep(2);
        // }, 1200);

//     return (
//         <div className="reset-form">
//             <h2>Create Your Account</h2>



//             <div className="form-group">
//                 <label htmlFor="email">Email Address</label>
//                 <input
//                     id="email"
//                     type="email"
//                     value={email}
//                     onChange={(e) => setEmail(e.target.value)}
//                     placeholder="Enter your email address"
//                     className={errors.email ? 'error' : ''}
//                 />
//                 {errors.email && <div className="error-message">{errors.email}</div>}
//             </div>
//             <div className="form-group">
//                 <label htmlFor="password">Password</label>
//                 <input
//                     id="password"
//                     type="password"
//                     value={password}
//                     onChange={(e) => setPassword(e.target.value)}
//                     placeholder="Create a password"
//                     autoComplete="new-password"
//                     className={errors.password ? 'error' : ''}
//                 />
//                 {errors.password && <div className="error-message">{errors.password}</div>}
//             </div>
//             <div className="form-group">
//                 <label htmlFor="confirmPassword">Confirm Password</label>
//                 <input
//                     id="confirmPassword"
//                     type="password"
//                     value={confirmPassword}
//                     onChange={(e) => setConfirmPassword(e.target.value)}
//                     placeholder="Confirm password"
//                     autoComplete="new-password"
//                     className={errors.confirmPassword ? 'error' : ''}
//                 />
//                 {errors.confirmPassword && <div className="error-message">{errors.confirmPassword}</div>}
//             </div>

//             <button
//                 className="btn primary full-width"
//                 onClick={handleSignUpSubmit}
//                 disabled={loading}
//             >
//                 {loading ? 'Creating Account...' : 'Sign Up'}
//             </button>
//         </div>
//     );
// } */