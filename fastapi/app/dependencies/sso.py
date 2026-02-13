from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.github import GithubSSO
from app.config import settings

GOOGLE_CLIENT_ID = settings.google_client_id or "your-google-client-id"
GOOGLE_CLIENT_SECRET = settings.google_client_secret or "your-google-client-secret"
VITE_BASE_API_URL = settings.vite_api_base_url or "http://localhost:56733/auth"


def get_google_sso():
    return GoogleSSO(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        redirect_uri=f"{VITE_BASE_API_URL}/auth/google/callback",
    )


def get_github_sso():
    return GithubSSO(
        client_id=settings.github_client_id,
        client_secret=settings.github_client_secret,
        redirect_uri=f"{VITE_BASE_API_URL}/auth/github/callback",
    )
