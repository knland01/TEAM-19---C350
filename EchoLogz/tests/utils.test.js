import { validateEmail, validatePassword, passwordsMatch } from "../frontend-react/src/utils.js";

test("validateEmail accepts well-formed emails", () => {
    expect(validateEmail("test@example.com")).toBe(true);
});

test("validateEmail rejects malformed emails", () => {
    expect(validateEmail("bad-email")).toBe(false);
    expect(validateEmail("a@b")).toBe(false);
});

test("validatePassword enforces length, alphanumerics, and no spaces", () => {
    expect(validatePassword("short1")).toBe(false);
    expect(validatePassword("has space 1")).toBe(false);
    expect(validatePassword("allletters")).toBe(false);
    expect(validatePassword("12345678")).toBe(false);
    expect(validatePassword("Valid123")).toBe(true);
});

test("passwordsMatch checks for equality", () => {
    expect(passwordsMatch("abc", "abc")).toBe(true);
    expect(passwordsMatch("abc", "abd")).toBe(false);
});
