from main import db, ma
from marshmallow import fields

class Employee(db.Model):
    # define the table name for the db
    __tablename__= "employees"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)  
    employee_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    roles = db.Column(db.String())
    is_admin = db.Column(db.Boolean, default=False)

    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    business = db.relationship("Business", back_populates="employees", cascade="all")

    jobs = db.relationship("Job", back_populates="employee", cascade="all")


class EmployeeSchema(ma.Schema):
    business = fields.Nested('BusinessSchema', only=['business_name'])
    jobs = fields.Nested('JobSchema', only=['id'])
    # roles = "employee" fields.Boolean()
    class Meta:
        fields = ('id', 'employee_name', 'email', 'business', 'roles', 'business_id', 'is_admin', 'password', 'jobs')


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)