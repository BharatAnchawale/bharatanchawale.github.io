# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env.production in the same directory
env_path = os.path.join(os.path.dirname(__file__), "..", ".env.production")
load_dotenv(dotenv_path=env_path)

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
