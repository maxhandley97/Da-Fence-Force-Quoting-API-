from flask import abort, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from main import db
from functools import wraps
from jwt.exceptions import InvalidTokenError

def manager_business_client_access():
    from blueprints.employees_bp import Employee
    from blueprints.businesses_bp import Business
    from blueprints.clients_bp import Client
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            jwt_identity = get_jwt_identity()
            claims = get_jwt()
            authorised_claim = claims.get("roles", [])
            if "manager" in authorised_claim:
                stmt = db.select(Employee).filter_by(id=jwt_identity)
            elif "business" in authorised_claim:
                stmt = db.select(Business).filter_by(id=jwt_identity)
            elif "client" in authorised_claim:
                stmt = db.select(Client).filter_by(id=jwt_identity)
            else:
                abort(401, description="Not authorised to access")

            user = db.session.scalar(stmt)
            if user.is_admin or any(role in authorised_claim for role in ["manager", "business", "client"]):
                return fn(*args, **kwargs)
            else:
                abort(401, description="Not authorised to access")

        return decorator

    return wrapper

def manager_business_access():
    from blueprints.employees_bp import Employee
    from blueprints.businesses_bp import Business
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            jwt_identity = get_jwt_identity()
            claims = get_jwt()
            authorised_claim = claims.get("roles", [])
            if "manager" in authorised_claim:
                stmt = db.select(Employee).filter_by(id=jwt_identity)
            elif "business" in authorised_claim:
                stmt = db.select(Business).filter_by(id=jwt_identity)
            else:
                abort(401, description="Not authorised to access")

            user = db.session.scalar(stmt)
            if user and (user.is_admin or any(role in authorised_claim for role in ["manager", "business", "client"])):
                return fn(*args, **kwargs)
            else:
                abort(401, description="Not authorised to access")

        return decorator

    return wrapper

# def manager_business_access(fn):
#     from blueprints.employees_bp import Employee
#     from blueprints.businesses_bp import Business

#     @wraps(fn)
#     def decorator(*args, **kwargs):
#         verify_jwt_in_request()
#         jwt_identity = get_jwt_identity()
#         claims = get_jwt()
#         authorised_claim = claims.get("roles", [])

#         # Check if 'business_id' is provided in the route parameters
#         business_id = kwargs.get("business_id")

#         if business_id:
#             # If 'business_id' is provided, check business authorization
#             if "business" not in authorised_claim:
#                 abort(401, description="Not authorised to access")

#             stmt = db.select(Business).filter_by(id=business_id)
#         else:
#             # If 'business_id' is not provided, check manager authorization
#             if "manager" not in authorised_claim:
#                 abort(401, description="Not authorised to access")

#             stmt = db.select(Employee).filter_by(id=jwt_identity)

#         user = db.session.scalar(stmt)

#         if user and (user.is_admin or any(role in authorised_claim for role in ["manager", "business", "client"])):
#             return fn(*args, **kwargs)
#         else:
#             abort(401, description="Not authorised to access")

#     return decorator

def authorised_business_or_manager(user_id=None):
    # Circular import issue
    from blueprints.employees_bp import Employee
    from blueprints.businesses_bp import Business
    try: 
        verify_jwt_in_request()
    except InvalidTokenError as e:
        abort(401, description=str(e))

    jwt_identity = get_jwt_identity()
    # Need to get JWT bearer information to see what database user belongs to
    claims = get_jwt()
    authorised_claim = claims.get("roles", [])
    if "manager" in authorised_claim:
        stmt = db.select(Employee).filter_by(id=jwt_identity)
    elif "business" in authorised_claim:
        stmt = db.select(Business).filter_by(id=jwt_identity)
    else:
        abort(401, description="Not authorised to access")
    user = None
    user = db.session.scalar(stmt)

    if not (user.is_admin or (user_id and jwt_identity == user_id)):
        abort(401, description="Not authorised to access")

def check_business_id(business_id):
    # Circular import issue
    from blueprints.employees_bp import Employee
    from blueprints.businesses_bp import Business
    try: 
        verify_jwt_in_request()
    except InvalidTokenError as e:
        abort(401, description=str(e))

    jwt_identity = get_jwt_identity()
    # Need to get JWT bearer information to see what database user belongs to
    claims = get_jwt()
    authorised_claim = claims.get("roles", [])
    if "manager" in authorised_claim:
        stmt = db.select(Employee).filter_by(id=jwt_identity)
        user = db.session.scalar(stmt)
        checked_business_id = user.business_id

    elif "business" in authorised_claim:
        stmt = db.select(Business).filter_by(id=jwt_identity)
        user = db.session.scalar(stmt)
        checked_business_id = user.id
    else:
        abort(401, description="Not authorised to access")
    if not user.is_admin or business_id == checked_business_id:
        abort(401, description="Not authorised to access")

def authorised_business_manager_client(user_id=None):
    # Circular import issue
    from blueprints.employees_bp import Employee
    from blueprints.businesses_bp import Business
    from blueprints.clients_bp import Client
    verify_jwt_in_request()
    jwt_identity = get_jwt_identity()
    # Need to get JWT bearer information to see what database user belongs to
    claims = get_jwt()
    authorised_claim = claims.get("roles", [])
    if "manager" in authorised_claim:
        stmt = db.select(Employee).filter_by(id=jwt_identity)
    elif "business" in authorised_claim:
        stmt = db.select(Business).filter_by(id=jwt_identity)
    elif "client" in authorised_claim:
        stmt = db.select(Client).filter_by(id=jwt_identity)
    else:
        abort(401, description="Not authorised to access")
    user = db.session.scalar(stmt)

    if not (user.is_admin or (user_id and jwt_identity == user_id)):
        abort(401, description="Not authorised to access")
    
# def employee_belongs_to_company


def authorised_business(business_id=None):
    from blueprints.businesses_bp import Business
    business_jwt = get_jwt_identity()

    stmt = db.select(Business).filter_by(id=business_jwt)
    business = db.session.scalar(stmt)
    
    if not (business.is_admin or (business_jwt and business_id == business_id)):
        abort(401, description="You are not an authorised business.")


def authorised_client(client_id=None):
    from blueprints.clients_bp import Client
    jwt_client_id = get_jwt_identity()

    stmt = db.select(Client).filter_by(id=jwt_client_id)
    client = db.session.execute(stmt).scalar()

    # Allow access if the client is an admin or if it's their own resource
    if not (client.is_admin or (client_id and jwt_client_id == client_id)):
        abort(401, description="You are not authorized to access this resource")

def get_business_id():
    from blueprints.employees_bp import Employee
    from blueprints.businesses_bp import Business
    try: 
        verify_jwt_in_request()
    except InvalidTokenError as e:
        abort(401, description=str(e))
    jwt_identity = get_jwt_identity()
    # Need to get JWT bearer information to see what database user belongs to
    claims = get_jwt()
    authorised_claim = claims.get("roles", [])
    if "manager" in authorised_claim:
        stmt = db.select(Employee).filter_by(id=jwt_identity)
        user = db.session.scalar(stmt)
        business_id = user.business_id

    elif "business" in authorised_claim:
        stmt = db.select(Business).filter_by(id=jwt_identity)
        user = db.session.scalar(stmt)
        business_id = user.id
    else: abort(401, description="Business ID can't be found in JWT")
    return business_id

