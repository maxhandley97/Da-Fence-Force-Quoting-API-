from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from main import db, bcrypt
from models.users import User, UserSchema, users_schema, user_schema
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import create_access_token
from datetime import timedelta
from setup import validation_error
from auth import authorise_business, authorise_user
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

users = Blueprint("users", __name__, url_prefix="/users")

@users.route("/register/", methods=["POST"])
@jwt_required()
def register_user():
    authorise_business()
    try:
        user_info = UserSchema(exclude=["id", "is_admin"]).load(request.json)
        is_manager = bool(user_info["is_manager"])
        business_id = user_info.get("business_id")


        user = User(
            user_name = user_info["user_name"],
            email = user_info["email"],
            password = bcrypt.generate_password_hash(user_info["password"]).decode("utf8"),
            is_manager = is_manager,
            business_id = business_id

        )
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude=["password", "is_admin"]).dump(user), 201

    except ValidationError as e:
        return validation_error(e)
    except ExpiredSignatureError:
        return {"error": "JWT token has expired"}, 422
    except InvalidTokenError:
        return {"error": "Invalid or missing JWT token in the Authorization header"}, 422
    except IntegrityError:
        return {"error": "User already signed up"}, 409
    except Exception as e:
        # Handle other exceptions if needed
        abort(401)
    
    
@users.route("/login/", methods=["POST"])
def login_as_user():
    user_info = UserSchema(only=["email", "password"]).load(request.json)
    stmt = db.select(User).where(User.email == user_info["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, user_info["password"]):
        token = create_access_token(identity=user.id, expires_delta=timedelta(weeks=2))
        return {"status": "successful login", "token": token, "user": UserSchema(exclude=["password"]).dump(user)}
    else:
        return {"error": "Invalid email or password"}, 401
    
# Get all useres
@users.route("/")
@jwt_required()
def all_users():
    # select * from cards;
    stmt = db.select(
        User)  # .where(db.or_(Card.status != "Done", Card.id > 2)).order_by(Card.title.desc())
    users = db.session.scalars(stmt).all()
      # Note: Set many=True to handle a collection of User objects
    return UserSchema(many=True, exclude=["password"]).dump(users)

@users.route("/<int:userId>", methods=["GET"])
# @jwt_required()
def get_user(userId):
    stmt = User.query.filter_by(id=userId)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema().dump(user)
    else:
        return {"error": "user not found"}, 404
    

@users.route("/<int:userId>", methods=["DELETE"])
def delete_user(userId):
    # authorise_business()
    #Parse incoming POST body through schema
    user = User.query.filter_by(id=userId).first()
    if user:
        username = user.user_name
        db.session.delete(user)
        db.session.commit()
        return {"Delete": f"Success! User {username} has been deleted."}, 201
    else:
        return {"error": "user not found"}, 404



@users.errorhandler(KeyError)
def key_error(e):
    return jsonify({'error': f'The field {e} is required'}), 400


