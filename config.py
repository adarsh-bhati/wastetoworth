import os

from dotenv import load_dotenv

load_dotenv()


# Flask

SECRET_KEY =os.getenv("SECRET_KEY")

# Uploads

UPLOAD_FOLDER = "static/uploads"

# Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# Database

DATABASE_NAME = "waste2worth.db"

# Allowed Extensions

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}