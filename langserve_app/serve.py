# langserve_app/serve.py
from fastapi import FastAPI
from langserve import add_routes
from app.services.openai_chat import get_response

app = FastAPI(title="LangServe Gateway")

add_routes(
    app,
    path="/langserve/chat",
    runnable=get_response
)
