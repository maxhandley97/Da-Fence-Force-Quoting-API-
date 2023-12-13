from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt_identity
from blueprints.businesses_bp import Business
from blueprints.employees_bp import Employee
from blueprints.clients_bp import Client

def client_or_business_required(*roles):
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
                (employee and (employee.is_admin or employee.manager)) or
                (client and client.id == jwt_user_id)
            ):
                abort(401, description="You are not authorized to access this resource.")

            return fn(*args, **kwargs)

        return decorator

    return wrapper