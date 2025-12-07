#!/usr/bin/env python3
"""One-time setup script for Google Tasks API authentication.

Usage:
    1. Go to https://console.cloud.google.com/
    2. Create a new project (or select existing)
    3. Enable "Google Tasks API"
    4. Go to "APIs & Services" > "Credentials"
    5. Create "OAuth 2.0 Client ID" (Desktop app)
    6. Download JSON and save as chat_assistant/credentials.json
    7. Run: python scripts/setup_google_auth.py
"""

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes for Google Tasks API
SCOPES = ["https://www.googleapis.com/auth/tasks"]

# Paths
BASE_DIR = Path(__file__).parent.parent / "chat_assistant"
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


def main():
    """Run OAuth flow and save token."""
    if not CREDENTIALS_FILE.exists():
        print(f"Error: {CREDENTIALS_FILE} not found!")
        print("\nPlease download OAuth credentials from Google Cloud Console:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Select your project")
        print("3. Go to 'APIs & Services' > 'Credentials'")
        print("4. Create 'OAuth 2.0 Client ID' (Desktop app)")
        print(f"5. Download JSON and save as {CREDENTIALS_FILE}")
        return

    creds = None

    # Check if token already exists
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # If no valid credentials, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Opening browser for authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for future use
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
        print(f"Token saved to {TOKEN_FILE}")

    print("\nAuthentication successful!")
    print("You can now use the Google Tasks integration.")


if __name__ == "__main__":
    main()
