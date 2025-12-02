import React from "react";
import { render, screen } from "@testing-library/react";
import '@testing-library/jest-dom';
import { MemoryRouter } from "react-router-dom";
import Navbar from "../frontend-react/src/components/Navbar.jsx";

test("renders Log In/Sign Up when signed out", () => {
    render(
        <MemoryRouter>
            <Navbar signedIn={false} username="" active="" />
        </MemoryRouter>
    );
    expect(screen.getByText("Log In")).toBeInTheDocument();
    expect(screen.getByText("Sign Up")).toBeInTheDocument();
});

test("renders Dashboard/History/Account/Musical Identity when signed in", () => {
    render(
        <MemoryRouter>
            <Navbar signedIn={true} username="TestUser" active="" />
        </MemoryRouter>
    );
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("History")).toBeInTheDocument(); // was "Saved"
    expect(screen.getByText("Account")).toBeInTheDocument();
    expect(screen.getByText("Musical Identity")).toBeInTheDocument(); // added
    expect(screen.getByText("Logout")).toBeInTheDocument(); // was "Sign Out"
});

test("applies active class correctly", () => {
    render(
        <MemoryRouter>
            <Navbar signedIn={true} username="TestUser" active="Dashboard" />
        </MemoryRouter>
    );
    const dashboard = screen.getByText("Dashboard");
    expect(dashboard.classList.contains("active")).toBe(true);
});
