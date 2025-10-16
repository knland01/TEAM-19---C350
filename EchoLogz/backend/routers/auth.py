"""
Authentication Router (The Gatekeeper)

This module defines all authentication-related API endpoints for the EchoLogz backend.
It manages user login, token verification, and integration with external OAuth providers
(such as Spotify) for secure access and authorization.

Core Responsibilities:
- Handle user login and logout routes
- Manage OAuth flows (Spotify authorization, callback, and token exchange)
- Issue and verify access tokens (JWT or session-based)
- Securely store and refresh tokens for authenticated users
- Enforce route protection for endpoints requiring authentication

Purpose:
Acts as the gatekeeper for the EchoLogz backend — responsible for verifying user identity, managing sessions, and enabling secure data access through token-based authentication.

Typical Usage Example:
    from fastapi import FastAPI
    from backend.routers import auth

    app = FastAPI()
    app.include_router(auth.router)
"""