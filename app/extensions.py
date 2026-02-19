# from flask_pymongo import PyMongo
# from flask_bcrypt import Bcrypt
# from flask_cors import CORS

# mongo = PyMongo()
# bcrypt = Bcrypt()
# cors = CORS()


from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager   # 🔥 ADD THIS

mongo = PyMongo()
bcrypt = Bcrypt()
cors = CORS()
jwt = JWTManager()   # 🔥 ADD THIS
