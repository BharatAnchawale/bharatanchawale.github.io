# keycloak_auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from auth.config import KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID
import requests

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fetch public Keycloak certs for token verification
def get_public_key():
    try:
        response = requests.get(
            f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"
        )
        jwks = response.json()["keys"][0]
        public_key = (
            "-----BEGIN PUBLIC KEY-----\n" + jwks["x5c"][0] + "\n-----END PUBLIC KEY-----"
        )
        return public_key
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to fetch Keycloak public key")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        public_key = get_public_key()
        payload = jwt.decode(token, public_key, algorithms=["RS256"], audience=KEYCLOAK_CLIENT_ID)
        return {
            "username": payload.get("preferred_username"),
            "email": payload.get("email"),
            "roles": payload.get("realm_access", {}).get("roles", [])
        }
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
