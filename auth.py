from flask import abort
from flask_jwt_extended import get_jwt_identity 
from main import db
from functools import wraps

def manager_required(*roles):
    from blueprints.businesses_bp import Business
    from blueprints.employees_bp import Employee
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            jwt_user_id = get_jwt_identity()

            # Check if the user is a business, employee manager, or an admin
            business = Business.query.get(jwt_user_id)
            user = Employee.query.get(jwt_user_id)

            if not ((business and business.id == jwt_user_id) or (user and (user.is_admin or user.is_manager))):
                abort(401, description="You are not authorised to access this resource.")

            return fn(*args, **kwargs)

        return decorator

    return wrapper


def client_or_business_required(*roles):
    from blueprints.businesses_bp import Business
    from blueprints.employees_bp import Employee
    from blueprints.clients_bp import Client
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            jwt_user_id = get_jwt_identity()

            # Check if the user is a business owner, employee manager, admin, or client
            business = Business.query.get(jwt_user_id)
            employee = Employee.query.get(jwt_user_id)
            client = Client.query.get(jwt_user_id)

            if not (
                (business and business.id == jwt_user_id) or
                (employee and (employee.is_admin or employee.is_manager)) or
                (client and client.id == jwt_user_id)
            ):
                abort(401, description="You are not authorized to access this resource.")

            return fn(*args, **kwargs)

        return decorator

def authorised_business(business_id=None):
    from blueprints.businesses_bp import Business
    jwt_business_id = get_jwt_identity()
    stmt = db.select(Business).filter_by(id=jwt_business_id)
    business = db.session.scalar(stmt)
    print(f"jwt_business_id: {jwt_business_id}, business_id: {business_id}")
    print(f"Business Object: {business}")
    # if its not the case that the business is an admin or business_id is truthy and matches the token
    # i.e if business_id isn"t passed in, they must be admin
    if not (business.is_admin or (business_id and jwt_business_id == business_id)):
        abort(401)

# def authorise_client(client_id=None):
#     from blueprints.clients_bp import Client
#     jwt_client_id = get_jwt_identity()
#     stmt = db.select(Client).filter_by(id=jwt_client_id)
#     client = db.session.execute(stmt).scalar()

#     if not (client and (client.is_admin or (client_id and jwt_client_id == client_id))):
#         abort(401, description="You are not authorized to access this resource")

def authorise_client(client_id=None):
    from blueprints.clients_bp import Client
    jwt_client_id = get_jwt_identity()
    print(f"JWT Client ID: {jwt_client_id}")

    stmt = db.select(Client).filter_by(id=jwt_client_id)
    client = db.session.execute(stmt).scalar()
    print(f"Client: {client}")

    # Allow access if the client is an admin or if it's their own resource
    if not (client and (client.is_admin or client.id == int(client_id))):
        print("Authorization failed.")
        abort(401, description="You are not authorized to access this resource")
    print("Authorization successful.")