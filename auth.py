from flask import abort
from flask_jwt_extended import get_jwt_identity 
from main import db
from blueprints.businesses_bp import Business

def authorise_business(business_id=None):
    jwt_business_id = get_jwt_identity()
    stmt = db.select(Business).filter_by(id=jwt_business_id)
    business = db.session.scalar(stmt)
    # if its not the case that the business is an admin or business_id is truthy and matches the token
    # i.e if business_id isn"t passed in, they must be admin
    if not (business.is_admin or (jwt_business_id and business_id == business_id)):
        abort(401)