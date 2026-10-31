import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    # Set SECRET_KEY in the hosting provider's environment before production.
    SECRET_KEY = os.environ.get("SECRET_KEY") or "local-development-key-change-before-deploy"
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
    elif DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or f"sqlite:///{BASE_DIR / 'instance' / 'farm.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024
    SITE_URL = os.environ.get("SITE_URL", "https://shreedogadabhumiraj.onrender.com")
