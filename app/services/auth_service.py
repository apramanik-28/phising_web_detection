import bcrypt
from flask_jwt_extended import create_access_token
from app.config.config import users_collection


class AuthService:

    @staticmethod
    def register_user(data):

        if not data.get("name") or not data.get("email") or not data.get("password"):
            return {"message": "All fields are required"}, 400

        existing_user = users_collection.find_one({"email": data["email"]})
        if existing_user:
            return {"message": "User already exists"}, 400

        hashed_password = bcrypt.hashpw(
            data["password"].encode("utf-8"),
            bcrypt.gensalt()
        )

        user = {
            "name": data["name"],
            "email": data["email"],
            "password": hashed_password
        }

        users_collection.insert_one(user)

        return {"message": "User registered successfully"}, 201

    @staticmethod
    def login_user(data):

        if not data.get("email") or not data.get("password"):
            return {"message": "Email and password required"}, 400

        user = users_collection.find_one({"email": data["email"]})

        if not user:
            return {"message": "User not found"}, 404

        if not bcrypt.checkpw(
            data["password"].encode("utf-8"),
            user["password"]
        ):
            return {"message": "Invalid password"}, 401

        access_token = create_access_token(identity=str(user["_id"]))

        return {
            "message": "Login successful",
            "access_token": access_token
        }, 200
