# import bcrypt
# from flask_jwt_extended import create_access_token
# #from app.config.config import users_collection
# from app.extensions import mongo


# class AuthService:

#     @staticmethod
#     def register_user(data):

#         if not data.get("name") or not data.get("email") or not data.get("password"):
#             return {"message": "All fields are required"}, 400

#         existing_user = users_collection.find_one({"email": data["email"]})
#         if existing_user:
#             return {"message": "User already exists"}, 400

#         hashed_password = bcrypt.hashpw(
#             data["password"].encode("utf-8"),
#             bcrypt.gensalt()
#         )

#         user = {
#             "name": data["name"],
#             "email": data["email"],
#             "password": hashed_password
#         }

#         users_collection.insert_one(user)

#         return {"message": "User registered successfully"}, 201

#     @staticmethod
#     def login_user(data):

#         if not data.get("email") or not data.get("password"):
#             return {"message": "Email and password required"}, 400

#         user = users_collection.find_one({"email": data["email"]})

#         if not user:
#             return {"message": "User not found"}, 404

#         if not bcrypt.checkpw(
#             data["password"].encode("utf-8"),
#             user["password"]
#         ):
#             return {"message": "Invalid password"}, 401

#         access_token = create_access_token(identity=str(user["_id"]))

#         return {
#             "message": "Login successful",
#             "access_token": access_token
#         }, 200

from app.extensions import mongo, bcrypt
from flask_jwt_extended import create_access_token
from bson import ObjectId
from datetime import datetime


class AuthService:

    # ==========================
    # REGISTER USER
    # ==========================
    @staticmethod
    def register_user(data):

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return {"message": "All fields are required"}, 400

        # Check if user already exists
        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            return {"message": "User already exists"}, 409

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Insert into DB
        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow()
        })

        return {"message": "User registered successfully"}, 201


    # ==========================
    # LOGIN USER
    # ==========================
    @staticmethod
    def login_user(data):

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password required"}, 400

        user = mongo.db.users.find_one({"email": email})

        if not user:
            return {"message": "User not found"}, 404

        if not bcrypt.check_password_hash(user["password"], password):
            return {"message": "Invalid credentials"}, 401

        # Create JWT token
        access_token = create_access_token(identity=str(user["_id"]))

        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"]
            }
        }, 200
