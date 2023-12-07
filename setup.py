from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError



app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = environ.get("JWT_KEY") #used to sign JWT
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URI") #database connection string
# avoid depreciation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) #connects two
ma = Marshmallow(app) #initialises, connects with flask
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
