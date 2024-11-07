from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Print the current working directory
logger.info(f"Current working directory: {os.getcwd()}")

from config import settings
from routers.v1 import audio_service

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

app.include_router(audio_service.router, prefix="/v1")