from main import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, Length, And

class Employee(db.Model):
    # define the table name for the db
    __tablename__= "employees"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    employee_id = db.Column(db.Integer,primary_key=True)  
    employee_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    roles = db.Column(db.String(), nullable=False, default="employee")
    is_admin = db.Column(db.Boolean, default=False)

    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    business = db.relationship("Business", back_populates="employees", cascade="all")

    jobs = db.relationship("Job", back_populates="employee", cascade="all")


class EmployeeSchema(ma.Schema):
    business = fields.Nested('BusinessSchema', only=['business_name'])
    jobs = fields.Nested('JobSchema', only=['id'])
    employee_name = fields.String(required=True, validate=Regexp('^[a-zA-Z ]+$', error="Title must contain only letters, numbers, and spaces"))
    email = fields.String(required=True, validate=Regexp('^\S+@\S+\.\S+$', error="Must be a valid email address"))
    password = fields.String(required=True, validate=And( 
        Length(min=8, error="Password must be at least 8 characters"),
        Regexp('^[0-9a-zA-Z]+$', error="Password must contain only letters and numbers")))
    
    # roles = "employee" fields.Boolean()
    class Meta:
        fields = ('id', 'employee_name', 'email', 'business', 'roles', 'business_id', 'is_admin', 'password', 'jobs')


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)