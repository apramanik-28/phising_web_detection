# import os
# from pymongo import MongoClient
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     MONGO_URI = os.getenv("MONGO_URI")
#     JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


# # MongoDB Connection
# client = MongoClient(Config.MONGO_URI)
# db = client["phishing_backend"]

# users_collection = db["users"]




import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
