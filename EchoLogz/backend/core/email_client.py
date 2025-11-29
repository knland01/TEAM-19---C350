"""
email_client.py
------------

DEVELOPMENT PLACEHOLDER ONLY.

Central module for all outbound user communication (email, SMS, etc.).

Future Responsibilities:
    - Send real verification emails
    - Send password reset messages
    - Render HTML templates
    - Integrate with a mail provider (SMTP / SendGrid / SES)

Current Behavior:
    - Simply prints verification URLs to console for development/testing.
"""

import asyncio


async def send_verification_email(to_email: str, verify_url: str) -> None:
    print("=== EMAIL DEBUG: Verification Email ===")
    print(f"To: {to_email}")
    print(f"Verify link: {verify_url}")
    print("=======================================")
    # Simulate network delay (SMTP, API call, etc.)
    await asyncio.sleep(0.1)