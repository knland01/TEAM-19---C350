/**
 * @jest-environment jsdom
 */

import { render, screen } from "@testing-library/react";
import Navbar from "../js/navbar.jsx";

test("renders Sign In/Sign Up when signed out", () => {
    render(<Navbar signedIn={false} username="" active="" />);
    expect(screen.getByText("Sign In")).toBeInTheDocument();
    expect(screen.getByText("Sign Up")).toBeInTheDocument();
});

test("renders Dashboard/Saved/Account when signed in", () => {
    render(<Navbar signedIn={true} username="TestUser" active="" />);
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Saved")).toBeInTheDocument();
    expect(screen.getByText("Account")).toBeInTheDocument();
    expect(screen.getByText("Sign Out")).toBeInTheDocument();
});

test("applies active class correctly", () => {
    render(<Navbar signedIn={true} username="TestUser" active="Dashboard" />);
    const dashboard = screen.getByText("Dashboard");
    expect(dashboard.classList.contains("active")).toBe(true);
});
