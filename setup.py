import os
from flask import jsonify, abort
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from werkzeug.exceptions import BadRequest

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # access to .env and get the value of SECRET_KEY, the variable name can be any but needs to match
    JWT_SECRET_KEY =  os.environ.get("SECRET_KEY")
    # JWT_TOKEN_LOCATION = ['headers', 'query_string']
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # access to .env and get the value of DATABASE_URL, the variable name can be any but needs to match
        value = os.environ.get("DATABASE_URL")

        if not value:
            raise ValueError("DATABASE_URL is not set")

        return value

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()


def unauthorized(err):
    return {"Authorisation error": "you are not authorised to access this resource"}, 401

def integrity_error(err):
    return {"Integrity error": "Duplicate record, already exists", "err":str(err)}, 409

def validation_error(err):
    return {"error": err.messages}, 400
def type_error(err):
    return {"error": "incorrect data type"}

def default_error(e):
    return jsonify({'error': e.description}), 400

def not_found_error(err):
    response = jsonify({"error": "Not Found", "message": "The requested URL was not found on the server."})
    response.status_code = 404
    return response

def key_error(e):
    return jsonify({'error': f'The field {e} is required'}), 400

def expired_signature_error(err):
        return {"error": "JWT token has expired"}, 422



def authorised_router_error_handler(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            return validation_error(e)
        except KeyError as e:
            return key_error(e)
        except ExpiredSignatureError:
            return {"error": "Your JWT token has expired"}, 401
        except InvalidTokenError:
            return {"error": "Invalid or missing JWT token in the Authorization header"}, 422
        except IntegrityError:
            return {"error": "Employee already signed up"}, 409
        except BadRequest as e:
            return default_error(e)
        # except Exception as e:
        #     abort(400)
    # need to
    inner.__name__ = f.__name__        
    return inner