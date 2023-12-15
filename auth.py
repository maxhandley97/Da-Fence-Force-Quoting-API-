from flask import abort, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
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

def manager_or_business():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["admin"] or claims["manager"] or claims["business"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper


def authorised_business_or_manager(user_id=None):
    # Circular import issue
    from blueprints.employees_bp import Employee
    from blueprints.businesses_bp import Business

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
    
    

# def authorised_business_or_manager(user_id=None):
#     # Circular import issue

#     from blueprints.employees_bp import Employee
#     from blueprints.businesses_bp import Business

#     jwt_identity = get_jwt_identity()
#     # Need to get JWT bearer information to see what database user belongs to
#     claims = get_jwt()
#     authorised_claim = claims.get("roles", [])
#     user = None
#     if "manager" in authorised_claim:
#         user = Employee.query.filter_by(id=jwt_identity).first()
#     elif "business" in authorised_claim:
#         user = Business.query.filter_by(id=jwt_identity).first()
#     else:
#         abort(401, description="Not authorised to access")

#     if not (user and (user.is_admin or (user_id and jwt_identity == user_id))):
#         abort(401, description="Not authorised to access")


# def authorised_business_or_manager():
#     # Circular import issue
#     from blueprints.employees_bp import Employee
#     from blueprints.businesses_bp import Business

#     jwt_identity = get_jwt_identity()
#     # Need to get JWT bearer information to see what database user belongs to
#     claims = get_jwt()
#     authorised_claim = claims.get("roles", [])

#     user = None
#     if "manager" in authorised_claim:
#         user = Employee.query.filter_by(id=jwt_identity).first()
#     elif "business" in authorised_claim:
#         user = Business.query.filter_by(id=jwt_identity).first()

#     if not (user and (user.is_admin or ["manager", "business"] in authorised_claim)):
#         abort(401, description="Not authorised to access")


# def employee_belongs_to_company


def authorised_business(business_id=None):
    from blueprints.businesses_bp import Business
    jwt_business_id = get_jwt_identity()
    
    stmt = db.select(Business).filter_by(id=business_id)
    business = db.session.scalar(stmt)
    
    if not (business.is_admin or (business_id and jwt_business_id == business_id)):
        abort(401, description="You are not an authorised business.")

def authorised_manager(employee_id=None):
    from blueprints.employees_bp import Employee
    jwt_employee_id = get_jwt_identity()
    
    stmt = db.select(Employee).filter_by(id=employee_id)
    employee = db.session.scalar(stmt)
    
    if not (employee.is_admin or (employee_id and jwt_employee_id == employee_id and employee.role == "manager")):
        abort(401, description="You are not an authorised employee.")

def authorised_client(client_id=None):
    from blueprints.clients_bp import Client
    jwt_client_id = get_jwt_identity()

    stmt = db.select(Client).filter_by(id=jwt_client_id)
    client = db.session.execute(stmt).scalar()

    # Allow access if the client is an admin or if it's their own resource
    if not (client and (client.is_admin and jwt_client_id == client_id)):
        abort(401, description="You are not authorized to access this resource")

# def is_authorised_business_or_manager(business_or_manager_id=None):
#     from blueprints.employees_bp import Employee
#     from blueprints.businesses_bp import Business
#     jwt_user_id = get_jwt_identity()

#     stmt = (db.select(Business).filter_by(id=jwt_user_id)) and (db.select(Employee).filter_by(id=jwt_user_id))
#     if stmt.count() > 1:


#     users = db.session.scalar(stmt)
#     print(users)
#     if not users.role == "manager" or users.role == "business" or users.is_admin:
#         abort(401, description="You are not authorized to access this resource")



def is_authorised_business_or_manager(business_or_manager_id=None):
    from blueprints.employees_bp import Employee
    from blueprints.businesses_bp import Business
    jwt_user_id = get_jwt_identity()

    # Try to find a Business with the given ID
    business = db.session.query(Business).filter_by(id=jwt_user_id).first()

    # If a Business is found, check authorization
    if business:
        if jwt_user_id == business.id:
            # Allow the business to perform actions on itself
            return business
        elif business.is_admin:
            abort(401, description="You are not authorized to access this resource.")

    # If no Business is found, try to find an Employee with the given ID
    employee = db.session.query(Employee).filter_by(id=jwt_user_id).first()

    # If an Employee is found, check authorization
    if employee:
        if jwt_user_id == employee.id:
            # Allow the employee to perform actions on itself
            return employee
        elif any(role in employee.roles for role in ['manager', 'business', 'admin']):
            # Check if the employee has the required roles
            return employee

    # If no Business or Employee is found or authorization fails
    abort(401, description="You are not authorized to access this resource.")
    # if user.role == "manager":


    # return user
    # try:
    #     stmt = db.select(Employee).filter_by(id=business_or_manager_id)
    #     user = db.session.scalar(stmt)
    #     return user
    # except:




    # # Check if the user has the required roles
    # if not user or not user.is_admin or not any(role in user.roles for role in ['manager', 'business', 'admin']):
    #     abort(401, description="You are not authorized to access this resource.")

# is_authorised_business_or_manager()