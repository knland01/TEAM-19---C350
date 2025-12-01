// src/pages/ErrorPage.jsx
import React from "react";
import Navbar from "../components/Navbar.jsx";
import "../pw-style.css";
import "../style_history.css";

export default function ErrorPage() {

  function BackButton() {
    function goBack() {
      window.history.back();
    }

    return (
      <button className="back-button" onClick={goBack}>
        Go Back
      </button>
    );
  }

  function ErrorPageContents() {
    return (
      <div className="reset-form">
        <h2>Error ___</h2>
        <p>Sorry :(</p>
        <p>Error Message</p>
        <BackButton />
      </div>
    );
  }

  return (
    
    <div className="app-container">
      <Navbar signedIn={false} />
      <div className="reset-container">
        <div className="reset-panel panel">
          <ErrorPageContents />
        </div>
      </div>
    </div>
  );
}