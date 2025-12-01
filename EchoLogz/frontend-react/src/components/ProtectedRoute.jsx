import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ signedIn, children }) {
    if (!signedIn) {
        return <Navigate to="/log_in" replace />;
    }
    return children;
}