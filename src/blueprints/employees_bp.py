from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from main import db, bcrypt
from models.employees import Employee, EmployeeSchema, employees_schema, employee_schema
from models.businesses import Business
from flask_jwt_extended import create_access_token
from datetime import timedelta
from setup import authorised_router_error_handler, invalid_token_error
from auth import authorised_business_or_manager
from jwt.exceptions import InvalidTokenError
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

employees = Blueprint("employees", __name__, url_prefix="/employees")


#Must be logged in as a business or a manager to register employees
@employees.route("/register/", methods=["POST"])
@jwt_required()
# @authorised_router_error_handler
def register_employee():
        employee_info = EmployeeSchema(exclude=["id", "is_admin"]).load(request.json)
        # Get the ID from JWT token
        try: 
            verify_jwt_in_request()
        except InvalidTokenError:
            abort(422)
            
        jwt_identity = get_jwt_identity()
        # looks at additional claims
        claims=get_jwt()
        #get the role from claims to accept both business and manager roles
        authorised_claim = claims.get("roles", [])
        if "manager" in authorised_claim:
             #Access the "business_id" from the "employee" dictionary
            employee_info = claims.get("employee", {})
            #need to instatiate the jwt to .get
            if isinstance(employee_info, dict):
                #get business_id for automation of employee information
                business_id = employee_info.get("business_id")
            else:
                abort(401)

        elif "business" in authorised_claim:
            #need to instatiate the jwt to .get
            if isinstance(jwt_identity, int):
                #get business_id for automation of employee information
                business_id = jwt_identity
        else:
            abort(401)

        #to make roles an optional input, defaulting to employee
        roles = employee_info.get("roles")
        phone = employee_info.get("phone", None)
        employee = Employee(
            employee_name = employee_info["employee_name"],
            email = employee_info["email"],
            password = bcrypt.generate_password_hash(employee_info["password"]).decode("utf8"),
            business_id = int(business_id),
            phone = phone,
            roles = roles
            
        )
        db.session.add(employee)
        db.session.commit()
        return EmployeeSchema(exclude=["password", "is_admin"]).dump(employee), 201

    
    

@employees.route("/login/", methods=["POST"])
@authorised_router_error_handler
def login_as_employee():
    employee_info = EmployeeSchema(only=["email", "password"]).load(request.json)
    stmt = db.select(Employee).where(Employee.email == employee_info["email"])
    employee = db.session.scalar(stmt)
    if employee and bcrypt.check_password_hash(employee.password, employee_info["password"]):
        if employee.roles == "manager":
            additional_claims = {"roles": "manager"}
        elif employee.roles == "employee":
            additional_claims = {"roles": "employee"}
        else:
            return {"error": "Invalid email or password"}, 401

        token = create_access_token(identity=employee.id, expires_delta=timedelta(weeks=2),additional_claims=additional_claims)
        return {"status": "successful login", "token": token, "employee": EmployeeSchema(exclude=["password", "is_admin"]).dump(employee)}
    else:
        return {"error": "Invalid email or password"}, 401
    
# Get all employeees
@employees.route("/")
@jwt_required()
def all_employees():
    authorised_business_or_manager() #only admin can access
    # select * from cards;
    stmt = db.select(
        Employee)  # .where(db.or_(Card.status != "Done", Card.id > 2)).order_by(Card.title.desc())
    employees = db.session.scalars(stmt).all()
      # Set many=True to handle a collection of Employee objects
    return EmployeeSchema(many=True, exclude=["password"]).dump(employees)

@employees.route("/<int:employeeId>", methods=["GET"])
@jwt_required()
def get_employee(employeeId):
    stmt = Employee.query.filter_by(id=employeeId)
    employee = db.session.scalar(stmt)
    if employee:
        return EmployeeSchema().dump(employee)
    else:
        return {"error": "employee not found"}, 404
    

@employees.route("/<int:employee_id>", methods=["DELETE"])
@jwt_required()
@authorised_router_error_handler
def delete_employee(employee_id):
    try:
        jwt_identity = get_jwt_identity()
        # looks at additional claims
        claims=get_jwt()
        #get the role from claims to accept both business and manager roles
        authorised_claim = claims.get("roles", [])
        if "manager" in authorised_claim:
            stmt = db.select(Employee).filter_by(id=jwt_identity)
            manager = db.session.scalar(stmt)
            business_id = manager.business_id
        elif "business" in authorised_claim:
            stmt = db.select(Business).filter_by(id=jwt_identity)
            business = db.session.scalar(stmt)
            business_id = business.id
        else:
            abort(401, description="Not authorised to access")
        logger.debug(f"auth: {authorised_claim}")

        stmt = db.select(Employee).filter_by(id=employee_id) # .where(Card.id == id)
        employee = db.session.scalar(stmt)
        #must be from the business 
        if employee and employee.business_id == business_id:
            logger.debug(f"Employee business_id: {employee.business_id}")
            logger.debug(f"Business_id: {business_id}")
            employee_name = employee.employee_name
            db.session.delete(employee)
            db.session.commit()
            return {"Delete": f"Success! Employee {employee_name} has been deleted."}, 201
        else:
            logger.debug(f"Employee business_id: {employee.business_id}")
            logger.debug(f"Business_id: {business_id}")
                            
            return {"error": "employee not found"}, 404
    except (Exception, AttributeError) as e:
        return invalid_token_error(e)
   
@employees.route("/<int:employee_id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorised_router_error_handler
def update_employee(employee_id):
    try:
        jwt_identity = get_jwt_identity()
        # looks at additional claims
        claims=get_jwt()
        #get the role from claims to accept both business and manager roles
        authorised_claim = claims.get("roles", [])
        if "manager" in authorised_claim:
            stmt = db.select(Employee).filter_by(id=jwt_identity)
            manager = db.session.scalar(stmt)
            business_id = manager.business_id
        elif "business" in authorised_claim:
            stmt = db.select(Business).filter_by(id=jwt_identity)
            business = db.session.scalar(stmt)
            business_id = business.id
        else:
            abort(401, description="Not authorised to access")
        employee_info = EmployeeSchema(exclude=["id", "business_id", "roles", "is_admin"]).load(request.json)

        stmt = db.select(Employee).filter_by(id=employee_id) # .where(Card.id == id)
        employee = db.session.scalar(stmt)
        #must be from the same business 
        if employee and employee.business_id == business_id:
            authorised_business_or_manager(business_id)
            employee.employee_name = employee_info.get("employee_name", employee.employee_name)
            employee.email = employee_info.get("email", employee.email)
            employee.password = employee_info.get("password", employee.password)
            employee.phone = employee_info.get("phone", employee.phone)
            db.session.commit()
            return {"Update Success": f"Business {employee.employee_name} has been updated.", 
                "Updated Details": EmployeeSchema(exclude=["password"]).dump(employee)}, 201
        else:
                            
            return {"error": "employee not found"}, 404
        
    except (Exception, AttributeError) as e:
        return {"error": str(e)}, 500
    #     return invalid_token_error(e)

