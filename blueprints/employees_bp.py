from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from main import db, bcrypt
from models.employees import Employee, EmployeeSchema, employees_schema, employee_schema
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import create_access_token
from datetime import timedelta
from setup import validation_error
from auth import manager_required
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

employees = Blueprint("employees", __name__, url_prefix="/employees")

@employees.route("/register/", methods=["POST"])
@jwt_required()
@manager_required('is_admin', 'is_manager', 'business')
def register_employee():
    
    try:
        employee_info = EmployeeSchema(exclude=["id", "is_admin"]).load(request.json)
        business_id = employee_info.get("business_id")


        employee = Employee(
            employee_name = employee_info["employee_name"],
            email = employee_info["email"],
            password = bcrypt.generate_password_hash(employee_info["password"]).decode("utf8"),
            #string is truthy, must add extra information for 
            is_manager = bool((employee_info["is_manager"]).lower() == "true"),
            business_id = business_id

        )
        db.session.add(employee)
        db.session.commit()
        return EmployeeSchema(exclude=["password", "is_admin"]).dump(employee), 201

    except ValidationError as e:
        return validation_error(e)
    except ExpiredSignatureError:
        return {"error": "JWT token has expired"}, 422
    except InvalidTokenError:
        return {"error": "Invalid or missing JWT token in the Authorization header"}, 422
    except IntegrityError:
        return {"error": "Employee already signed up"}, 409
    except Exception as e:
        # Handle other exceptions if needed
        abort(401)
    
    
@employees.route("/login/", methods=["POST"])
def login_as_employee():
    employee_info = EmployeeSchema(only=["email", "password"]).load(request.json)
    stmt = db.select(Employee).where(Employee.email == employee_info["email"])
    employee = db.session.scalar(stmt)
    if employee and bcrypt.check_password_hash(employee.password, employee_info["password"]):
        token = create_access_token(identity=employee.id, expires_delta=timedelta(weeks=2))
        return {"status": "successful login", "token": token, "employee": EmployeeSchema(exclude=["password"]).dump(employee)}
    else:
        return {"error": "Invalid email or password"}, 401
    
# Get all employeees
@employees.route("/")
@jwt_required()
def all_employees():
    # select * from cards;
    stmt = db.select(
        Employee)  # .where(db.or_(Card.status != "Done", Card.id > 2)).order_by(Card.title.desc())
    employees = db.session.scalars(stmt).all()
      # Note: Set many=True to handle a collection of Employee objects
    return EmployeeSchema(many=True, exclude=["password"]).dump(employees)

@employees.route("/<int:employeeId>", methods=["GET"])
# @jwt_required()
def get_employee(employeeId):
    stmt = Employee.query.filter_by(id=employeeId)
    employee = db.session.scalar(stmt)
    if employee:
        return EmployeeSchema().dump(employee)
    else:
        return {"error": "employee not found"}, 404
    

@employees.route("/<int:employeeId>", methods=["DELETE"])
def delete_employee(employeeId):
    # authorise_business()
    #Parse incoming POST body through schema
    employee = Employee.query.filter_by(id=employeeId).first()
    if employee:
        employeename = employee.employee_name
        db.session.delete(employee)
        db.session.commit()
        return {"Delete": f"Success! Employee {employeename} has been deleted."}, 201
    else:
        return {"error": "employee not found"}, 404



@employees.errorhandler(KeyError)
def key_error(e):
    return jsonify({'error': f'The field {e} is required'}), 400


