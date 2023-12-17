from main import db, ma
from marshmallow import fields

class Business(db.Model):
    # define the table name for the db
    __tablename__= "businesses"
    #primary key
    id = db.Column(db.Integer,primary_key=True)  

    business_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    abn = db.Column(db.BigInteger(), nullable=False, unique=True)
    roles = db.Column(db.String(), nullable=False, default="business")
    is_admin = db.Column(db.Boolean, default=False)

    employees = db.relationship("Employee", back_populates="business", cascade="all, delete-orphan")
    quotes = db.relationship("Quote", back_populates="business", cascade="all, delete-orphan")
    jobs = db.relationship("Job", back_populates="business", cascade="all, delete-orphan")

class BusinessSchema(ma.Schema):
    employees = fields.Nested("EmployeeSchema", only=["employee_name"], many=True)
    class Meta:
        fields = ('id', 'business_name', 'email', 'password', 'abn', 'is_admin', 'employee_name', 'roles')

business_schema = BusinessSchema()
businesses_schema = BusinessSchema(many=True)