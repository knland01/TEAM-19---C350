export function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

export function validatePassword(password) {
    if (password.length < 8 ||
        /\s/.test(password) ||
        !/[A-Za-z]/.test(password) ||
        !/[0-9]/.test(password)
    ) {
        return false;
    }
    return true;
}

export function passwordsMatch(password, confirmPassword) {
    return password === confirmPassword;
}