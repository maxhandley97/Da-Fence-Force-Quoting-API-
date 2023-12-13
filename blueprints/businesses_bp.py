from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db, bcrypt
from models.businesses import Business, BusinessSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta
from auth import authorised_business

business = Blueprint("business", __name__, url_prefix="/business")

@business.errorhandler(KeyError)
def key_error(e):
    return jsonify({'error': f'The field {e} is required'}), 400

@business.route("/register", methods=["POST"])
def register_business():
    try:
        business_info = BusinessSchema(exclude=["id", "is_admin"]).load(request.json)
        business = Business(
            business_name = business_info["business_name"],
            email = business_info["email"],
            password = bcrypt.generate_password_hash(business_info["password"]).decode("utf8"),
            abn = business_info["abn"]
        )
        db.session.add(business)
        db.session.commit()
        return BusinessSchema(exclude=["password"]).dump(business), 201

    except IntegrityError:
        return {"error": "Business already signed up"}, 409
    
@business.route("/login/", methods=["POST"])
def login_as_business():
    business_info = BusinessSchema(only=["email", "password"]).load(request.json)
    stmt = db.select(Business).where(Business.email == business_info["email"])
    business = db.session.scalar(stmt)
    if business and bcrypt.check_password_hash(business.password, business_info["password"]):
        token = create_access_token(identity=business.id, expires_delta=timedelta(weeks=2))
        return {"status": "successful login", "token": token, "Business": BusinessSchema(exclude=["password"]).dump(business)}
    else:
        return {"error": "Invalid email or password"}, 401
    
# Get all businesses
@business.route("/")
@jwt_required()
def all_businesses():
    # select * from cards;
    stmt = db.select(
        Business
    )  # .where(db.or_(Card.status != "Done", Card.id > 2)).order_by(Card.title.desc())
    businesses = db.session.scalars(stmt).all()
    return BusinessSchema(many=True, exclude=[]).dump(businesses)

@business.route("/<int:business_id>", methods=["DELETE"])
@jwt_required()
def delete_business(business_id):
    authorised_business(business_id)
    business = Business.query.get(business_id)
    if business:
        businessname = business.business_name
        db.session.delete(business)
        db.session.commit()
        return {"Delete": f"Success! Business {businessname} has been deleted."}, 201
    else:
        return {"error": "business not found"}, 404

    return "Success", 201




