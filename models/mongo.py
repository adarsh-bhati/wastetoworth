from pymongo import MongoClient
from config import MONGO_URI

# ==========================
# CONNECT TO ATLAS
# ==========================

client = MongoClient(MONGO_URI)

# ==========================
# DATABASE
# ==========================

db = client["worth"]

# ==========================
# COLLECTIONS
# ==========================

users_collection = db["users"]

projects_collection = db["projects"]

# ==========================
# USER FUNCTIONS
# ==========================

def create_user(user_data):

    return users_collection.insert_one(
        user_data
    )


def get_user_by_email(email):

    return users_collection.find_one(
        {
            "email": email
        }
    )


def get_user_by_id(user_id):

    return users_collection.find_one(
        {
            "_id": user_id
        }
    )


# ==========================
# PROJECT FUNCTIONS
# ==========================

def save_project(project):

    return projects_collection.insert_one(
        project
    )


def get_user_projects(user_id):

    projects = projects_collection.find(
        {
            "user_id": user_id
        }
    ).sort(
        "created_at",
        -1
    )

    return list(projects)


def get_project_by_id(project_id):

    from bson import ObjectId

    return projects_collection.find_one(
        {
            "_id": ObjectId(project_id)
        }
    )


# ==========================
# CONNECTION TEST
# ==========================

def test_connection():

    try:

        client.admin.command(
            "ping"
        )

        print(
            "MongoDB Connected Successfully"
        )

    except Exception as e:

        print(
            f"MongoDB Error: {e}"
        )


if __name__ == "__main__":

    test_connection()