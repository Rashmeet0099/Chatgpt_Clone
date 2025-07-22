from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.routes import users, chat
from app.database import Base, engine

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this if you want to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables
Base.metadata.create_all(bind=engine)

# Include your route modules
app.include_router(users.router)
app.include_router(chat.router)

# --- Custom OpenAPI for Swagger: Add X-Username header to POST/PUT endpoints ---
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="ChatGPT Clone API",
        version="1.0.0",
        description="API for chatting and user management",
        routes=app.routes,
    )

    # Add X-Username header support to Swagger docs
    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "requestBody" in method:
                method.setdefault("parameters", []).append({
                    "name": "X-Username",
                    "in": "header",
                    "required": True,
                    "schema": {"type": "string"},
                    "description": "Your registered username"
                })

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


