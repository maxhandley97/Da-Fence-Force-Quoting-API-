from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db, bcrypt
from models.businesses import Business, BusinessSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from blueprints.jobs_bp import jobs
from datetime import timedelta
from auth import manager_business_access, authorised_business
from setup import authorised_router_error_handler

business = Blueprint("business", __name__, url_prefix="/business")

business.register_blueprint(jobs)

@business.route("/register", methods=["POST"])
@authorised_router_error_handler
def register_business():
    try:
        business_info = BusinessSchema(exclude=["id", "is_admin", "roles"]).load(request.json)
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
@authorised_router_error_handler
def login_as_business():
    business_info = BusinessSchema(only=["email", "password"]).load(request.json)
    stmt = db.select(Business).where(Business.email == business_info["email"])
    business = db.session.scalar(stmt)
    if business and bcrypt.check_password_hash(business.password, business_info["password"]):
        additional_claims = {"roles": "business"}
        token = create_access_token(
            identity=business.id, 
            expires_delta=timedelta(weeks=2), 
            additional_claims=additional_claims)
        return {"status": "successful login", "token": token, "Business": BusinessSchema(exclude=["password", "is_admin", "roles"]).dump(business)}
    else:
        return {"error": "Invalid email or password"}, 401
    
# Get all businesses
@business.route("/")
@jwt_required()
@manager_business_access()
@authorised_router_error_handler
@manager_business_access()
def all_businesses():
    # select * from businesses;
    stmt = db.select(
        Business
    ) 
    businesses = db.session.scalars(stmt).all()
    return jsonify(BusinessSchema(many=True, exclude=["password"]).dump(businesses))

@business.route("/<int:business_id>", methods=["DELETE"])
@jwt_required()
@authorised_router_error_handler
def delete_business(business_id):
    business = Business.query.get(business_id)
    if business:
        authorised_business(business_id)
        businessname = business.business_name
        db.session.delete(business)
        db.session.commit()
        return {"Delete": f"Success! Business {businessname} has been deleted."}, 201
    else:
        return {"error": "business not found"}, 404

@business.route("/<int:business_id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorised_router_error_handler
def update_business(business_id):
    business_info = BusinessSchema(exclude=["id", "is_admin", "roles"]).load(request.json)
    stmt = db.select(Business).filter_by(id=business_id)
    business = db.session.scalar(stmt)
    if business:
        authorised_business(business_id)
        business.business_name = business_info.get("business_name", business.business_name)
        business.email = business_info.get("email",business.email)
        business.password = business_info.get("password",business.password)
        business.abn = business_info.get("abn",business.abn)
        db.session.commit()
        return {"Update Success": f"Business {business.business_name} has been updated.", 
                "Updated Details": BusinessSchema(exclude=["password"]).dump(business)}, 201
    else:
        return {"error": "business not found"}, 404


