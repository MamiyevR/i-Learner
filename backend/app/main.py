from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import upload, generate, chat, session, feedback

app = FastAPI()

# Enable CORS for all origins (configured for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(upload.router)
app.include_router(generate.router)
app.include_router(feedback.router)
app.include_router(chat.router)
app.include_router(session.router)


@app.get("/")
def root():
    return {"message": "AI Assessment Tool Backend"}
