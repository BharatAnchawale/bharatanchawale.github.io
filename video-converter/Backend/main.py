# main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from auth.keycloak_auth import get_current_user

app = FastAPI(title="Video Converter Backend")

# Allow Swagger to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {
        "message": f"Hello, {user['username']}! You are authenticated.",
        "roles": user["roles"]
    }
