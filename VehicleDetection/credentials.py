"""Resolve a Google service-account key without storing it in git."""

import os

LOCAL_KEYFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")

SHEETS_SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


def service_account_path():
    """Path to the service-account JSON key.

    ``GOOGLE_APPLICATION_CREDENTIALS`` wins. Otherwise the gitignored file
    ``VehicleDetection/credentials.json`` is used.
    """
    path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or LOCAL_KEYFILE
    if not os.path.isfile(path):
        raise FileNotFoundError(
            "Google service-account key not found. Set "
            "GOOGLE_APPLICATION_CREDENTIALS to the JSON key file, or place "
            "that file at VehicleDetection/credentials.json (gitignored)."
        )
    return path


def load_gspread_client():
    """Authorize gspread with the service-account key from :func:`service_account_path`."""
    import gspread
    from google.oauth2.service_account import Credentials

    creds = Credentials.from_service_account_file(
        service_account_path(), scopes=SHEETS_SCOPES
    )
    return gspread.authorize(creds)
