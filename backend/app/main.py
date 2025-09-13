from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import auth, journals, ai, progress

# This line creates the database tables.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS Middleware Configuration ---
# This is the crucial part to fix the frontend connection errors.
# It tells the browser that it's safe for your frontend to make requests to this backend.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, ["*"] allows all origins. For production, you should restrict this to your frontend's domain, e.g., ["https://www.lingojourn.com"].
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, etc.).
    allow_headers=["*"],  # Allows all headers (including Authorization).
)
# --- End of CORS Configuration ---


@app.get("/")
def read_root():
    return {"message": "Welcome to the LingoJourn API!"}


# Include the routers from other files
app.include_router(auth.router)
app.include_router(journals.router)
app.include_router(ai.router)
app.include_router(progress.router)

