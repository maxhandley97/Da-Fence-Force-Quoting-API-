from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db, bcrypt
from models.users import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta
from auth import authorise_business

users = Blueprint("users", __name__, url_prefix="/users")

@users.errorhandler(KeyError)
def key_error(e):
    return jsonify({'error': f'The field {e} is required'}), 400

@users.route("/register", methods=["POST"])
def register_user():
    # authorise_business()
    try:
        user_info = UserSchema(exclude=["id", "is_admin"]).load(request.json)
        user = User(
            user_name = user_info["user_name"],
            email = user_info["email"],
            password = bcrypt.generate_password_hash(user_info["password"]),
            abn = user_info["abn"]
        )
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude=["password"]).dump(user), 201

    except IntegrityError:
        return {"error": "User already signed up"}, 409
    
@users.route("/login/", methods=["POST"])
def login_as_user():
    user_info = UserSchema(only=["email", "password"])
    stmt = db.select(User).where(User.email == user_info["email"]).first()
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
    return UserSchema(exclude=["password"]).dump(users)

@users.route("/<userId>", methods=["GET"])
@jwt_required()
def get_user(userId):
    stmt = User.query.filter_by(id=userId)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema().dump(user)
    else:
        return {"error": "user not found"}, 404
    

@users.route("/<userId>", methods=["DELETE"])
def delete_user(userId):
    authorise_business()
    #Parse incoming POST body through schema
    User.query.filter_by(id=userId).delete()
   
    db.session.commit()

    return "Success", 201




