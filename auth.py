from flask import abort
from flask_jwt_extended import get_jwt_identity 
from main import db
from functools import wraps

def roles_required(*roles):
    from blueprints.businesses_bp import Business
    from blueprints.employees_bp import Employee
    from blueprints.clients_bp import Client
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            jwt_user_id = get_jwt_identity()

            # Check if the user has the required roles
            user = Business.query.get(jwt_user_id) or Client.query.get(jwt_user_id) or Employee.query.get(jwt_user_id)

            if not user or not user.is_admin or not any(role in user.roles for role in roles):
                abort(401, description="You are not authorized to access this resource.")

            return fn(*args, **kwargs)

        return decorator

    return wrapper


def authorised_business(business_id=None):
    from blueprints.businesses_bp import Business
    jwt_business_id = get_jwt_identity()
    
    if business_id and jwt_business_id == business_id:
        # Allow the business to delete itself
        return
    
    business = Business.query.get(jwt_business_id)
    
    if business is None or not business.is_admin:
        abort(401, description="You are not authorized to delete this business.")

def authorised_client(client_id=None):
    from blueprints.clients_bp import Client
    jwt_client_id = get_jwt_identity()

    stmt = db.select(Client).filter_by(id=jwt_client_id)
    client = db.session.execute(stmt).scalar()

    # Allow access if the client is an admin or if it's their own resource
    if not (client and (client.is_admin or client.id == int(client_id))):
        abort(401, description="You are not authorized to access this resource")
    