from app.extensions import mongo

class UserModel:

    @staticmethod
    def create_user(data):
        return mongo.db.users.insert_one(data)

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})
