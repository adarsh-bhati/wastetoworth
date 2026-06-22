from flask import Flask, render_template, request,redirect
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from bson import ObjectId

import bcrypt
from models.user_model import User

from groq import Groq
import os
#from models.detector import detect_materials
from models.gemini_detector import (
    detect_materials_with_gemini
)
from config import GROQ_API_KEY
"""from models.database import (
    create_tables,
    save_project,
    get_projects,
    get_project_by_id
)"""
from models.mongo import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_user_projects,
    save_project,
    get_project_by_id,
    users_collection,
    projects_collection
)
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"
#create_tables()

@login_manager.user_loader

def load_user(user_id):

    user_data = get_user_by_id(
        ObjectId(user_id)
    )

    if user_data:

        return User(user_data)

    return None
client = Groq(
    api_key=GROQ_API_KEY
)

# ==========================
# HOME
# ==========================

@app.route("/")
@login_required
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "GET":

        return render_template(
            "signup.html"
        )

    username = request.form["username"]

    email = request.form["email"]

    password = request.form["password"]

    existing_user = get_user_by_email(
        email
    )

    if existing_user:

        return render_template(
            "signup.html",
            error="Email already exists."
        )

    hashed_password = bcrypt.hashpw(

        password.encode("utf-8"),

        bcrypt.gensalt()

    )

    create_user({

        "username": username,

        "email": email,

        "password": hashed_password

    })

    return render_template(
        "login.html",
        error="Account created successfully. Please login."
    )
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":

        return render_template(
            "login.html"
        )

    email = request.form["email"]

    password = request.form["password"]

    user_data = get_user_by_email(
        email
    )

    if not user_data:

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    password_ok = bcrypt.checkpw(

        password.encode("utf-8"),

        user_data["password"]

    )

    if not password_ok:

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    user = User(user_data)

    login_user(user)

    return redirect("/")
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/")
# ==========================
# UPLOAD PAGE
# ==========================

@app.route("/upload")
@login_required
def upload():
    return render_template("upload.html")


# ==========================
# MANUAL PAGE
# ==========================

@app.route("/manual")
@login_required
def manual():
    return render_template("manual.html")


# ==========================
# GENERATE PROJECT
# ==========================

@app.route("/generate", methods=["POST"])
@login_required
def generate():

    materials = request.form.getlist("materials[]")

    materials = [m.strip() for m in materials if m.strip()]
    if not materials:

     return render_template(
        "manual.html",
        error="Please enter at least one material."
     )
    material_text = "\n".join(materials)

    prompt = f"""
You are an eco-friendly DIY expert.

Materials Available:
{material_text}

Generate ONE creative project.

Return response in this exact format:

Project Name:
Description:
Difficulty:
Build Time:
Materials:
Steps:
Safety Tips:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.8

    )

    ai_text = response.choices[0].message.content

    project = parse_ai_response(
        ai_text,
        materials
    )
    project["user_id"] = str(current_user.id)

    save_project(project)
    return render_template(
        "result.html",
        project=project
    )


# ==========================
# AI RESPONSE PARSER
# ==========================

def parse_ai_response(text, materials):

    project = {

        "project_name": "Eco Project",

        "description": "",

        "difficulty": "Easy",

        "build_time": "30 Minutes",

        "materials": materials,

        "steps": [],

        "safety_tips": "",

        "waste_reused": f"{len(materials)} Items",

        "co2_saved": round(len(materials) * 0.15, 2),

        "landfill_reduction": round(len(materials) * 0.30, 2)

    }

    lines = text.split("\n")

    current_section = None

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        if lower.startswith("project name"):
            project["project_name"] = line.split(":",1)[1].strip()

        elif lower.startswith("description"):
            project["description"] = line.split(":",1)[1].strip()

        elif lower.startswith("difficulty"):
            project["difficulty"] = line.split(":",1)[1].strip()

        elif lower.startswith("build time"):
            project["build_time"] = line.split(":",1)[1].strip()

        elif lower.startswith("safety tips"):
            project["safety_tips"] = line.split(":",1)[1].strip()

        elif lower.startswith("steps"):
            current_section = "steps"

        elif current_section == "steps":

            if line and ( line.startswith("-") or line[0].isdigit()):
                project["steps"].append(line)

    if len(project["steps"]) == 0:

        project["steps"] = [

            "Prepare all materials",

            "Cut and shape components",

            "Assemble structure",

            "Decorate and finish",

            "Use your eco-friendly project"

        ]

    return project


# ==========================
# DEMO RESULT PAGE
# ==========================

@app.route("/result/<project_id>")
@login_required
def project_detail(project_id):

    row = get_project_by_id(project_id)


    if not row:
        return "Project Not Found"

    project = {

        "project_name": row["project_name"],
        "description": row["description"],
        "difficulty": row["difficulty"],
        "build_time": row["build_time"],

        "materials": row["materials"],

        "steps": row["steps"],

        "safety_tips": row["safety_tips"],

        "waste_reused": row["waste_reused"],

        "co2_saved": row["co2_saved"],

        "landfill_reduction": row["landfill_reduction"]

    }

    return render_template(
        "result.html",
        project=project
    )

@app.route("/detect", methods=["POST"])
@login_required
def detect():

    image = request.files.get("image")

    if not image or image.filename == "":
      return render_template(
        "upload.html",
        error="Please select an image."
      )

    UPLOAD_FOLDER = "static/uploads"

    os.makedirs(
      UPLOAD_FOLDER,
      exist_ok=True
    )

    upload_path = os.path.join(
      UPLOAD_FOLDER,
      image.filename
    )

    image.save(upload_path)

    """materials = detect_materials(
        upload_path
    )"""
    materials = detect_materials_with_gemini(
      upload_path
    )

    return render_template(
        "detected.html",
        materials=materials,
        image_path="/" + upload_path
    )
@app.route("/history")
@login_required
def history():

    projects = get_user_projects(
        str(current_user.id)
    )

    return render_template(
        "history.html",
        projects=projects
    )
@app.route("/generate-again")
@login_required
def generate_again():

    return redirect("/manual")
if __name__ == "__main__":
    app.run(
        debug=True
    )