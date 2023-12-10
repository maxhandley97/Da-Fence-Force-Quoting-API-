from flask import abort
from flask_jwt_extended import get_jwt_identity 
from main import db
# from blueprints.businesses_bp import Business
# from blueprints.employees_bp import Employee

from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import abort

def roles_required(*roles):
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
                abort(401, description="You are not authorized to access this resource.")

            return fn(*args, **kwargs)

        return decorator

    return wrapper








def authorise_create_employee(employee_id=None, business_id=None):
    from blueprints.businesses_bp import Business
    from blueprints.employees_bp import Employee
    jwt_user_id = get_jwt_identity()

    user = Employee.query.get(jwt_user_id)
    business = Business.query.get(jwt_user_id)

    # Fetch the user from the database based on the user_id in the JWT
    # user_jwt = Employee.query.get(jwt_user_id)
    # business_jwt = Business.query.get(jwt_user_id)
    # stmt1 = db.select(Business).filter_by(id=jwt_user_id)
    # business = db.session.scalar(stmt1)

    # stmt2 = db.select(Employee).filter_by(id=jwt_user_id)
    # user = db.session.scalar(stmt2)
    # db.session.commit()

    # business = Business.query.get(jwt_user_id)
    # stmt = db.select(Employee).filter_by(id=jwt_user_id)
    # user = db.session.scalar(stmt)
    print(f"jwt_user_id: {jwt_user_id}")
    print(f"Business Object: {business}")
    print(f"User Object: {user}")

    # Check if the user is a business, employee manager, or an admin
    if not ((business and jwt_user_id == business_id) or (user and (user.is_admin or user.is_manager) and jwt_user_id == employee_id)):
        abort(401, description="You are not authorized to create a new employee.")

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

# def authorise_employee(employee_id=None, business_id=None):
#     jwt_user_id = get_jwt_identity()
#     try:
#         if business_id:
#             # If business_id is provided, check against the Business database
#             stmt = db.select(Business).filter_by(id=jwt_user_id)
#             user = db.session.scalar(stmt)
#         elif employee_id:
#             # If employee_id is provided, check against the Employee database
#             user = Employee.query.get(jwt_user_id)
#         else:
#             # If neither business_id nor employee_id is provided, raise an error
#             raise ValueError("Either business_id or employee_id must be provided.")
        
#     except NoResultFound:
#         raise PermissionError("User not found.")
#     # Fetch the employee from the database based on the employee_id in the JWT
    
#     # Check if the employee is an admin or if the provided employee_id matches the one in the token
#     if not (employee.is_admin or employee.is_manager or (jwt_employee_id and employee_id == jwt_employee_id)):
#         abort(401)