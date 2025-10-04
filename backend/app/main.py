from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import auth, journals, ai, progress, admin, notifications
import os

# This line creates the database tables.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS Middleware Configuration ---
# This is the crucial part to fix the frontend connection errors.
# It tells the browser that it's safe for your frontend to make requests to this backend.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://it.parasyst.com", "https://ti.parasyst.com", "https://ipa.parasyst.com", "http://localhost:3000", "http://ai-ndhu-lab:3000"],  # For development, ["*"] allows all origins. For production, you should restrict this to your frontend's domain, e.g., ["https://www.lingojourn.com"].
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, etc.).
    allow_headers=["*"],  # Allows all headers (including Authorization).
)
# --- End of CORS Configuration ---

# --- Static Files Configuration ---
# This section sets up a directory to serve static files like images.

# Create a path to the 'static' directory.
# os.path.dirname(__file__) gets the directory of the current file (main.py).
# We then join it with 'static' to create a full path.
static_files_dir = os.path.join(os.path.dirname(__file__), "static")

# Create the directories if they don't exist to prevent errors on first run.
os.makedirs(static_files_dir, exist_ok=True)
os.makedirs(os.path.join(static_files_dir, "uploads"), exist_ok=True) # Ensure uploads folder exists

# Mount the 'static' directory to the '/static' URL path.
# Any file inside 'app/static/' will be accessible from '/static/'.
# For example, a file at 'app/static/images/logo.png' will be available at
# 'http://your-api-url/static/images/logo.png'
app.mount("/static", StaticFiles(directory=static_files_dir), name="static")
# --- End of Static Files Configuration ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the LingoJourn API!"}


# Include the routers from other files
app.include_router(auth.router)
app.include_router(journals.router)
app.include_router(ai.router)
app.include_router(progress.router)
app.include_router(admin.router)
app.include_router(notifications.router)
