from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from setup import integrity_error, validation_error, unauthorized, not_found_error



db = SQLAlchemy() #connects two
ma = Marshmallow() #initialises, connects with flask
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    # using a list comprehension and multiple assignment 
    # to grab the environment variables we need
    
    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    # configuring our app:
    app.config.from_object("setup.app_config")

    # creating our database object! This allows us to use our ORM
    db.init_app(app)
    
    # creating our marshmallow object! This allows us to use schemas
    ma.init_app(app)

    #creating the jwt and bcrypt objects! this allows us to use authentication
    bcrypt.init_app(app)
    jwt.init_app(app)

    from blueprints.cli_bp import db_commands
    app.register_blueprint(db_commands)

    # import the controllers and activate the blueprints
    from blueprints import registerable_blueprints

    for controller in registerable_blueprints:
        app.register_blueprint(controller)

    @app.errorhandler(Exception)
    def handle_error(error):
        status_code = getattr(error, 'code', 500)  # Get the status code if available
        response = jsonify({"error": "Internal Server Error", "message": str(error)})
        response.status_code = status_code
        return response
    
    app.errorhandler(401)(unauthorized)
    app.errorhandler(IntegrityError)(integrity_error)
    app.errorhandler(ValidationError)(validation_error)
    app.register_error_handler(404, not_found_error)

    
    return app





