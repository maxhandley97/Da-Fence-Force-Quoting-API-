from main import db, ma
from marshmallow import fields

class Job(db.Model):
    # define the table name for the db
    __tablename__= "jobs"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)  
    estimated_start = db.Column(db.Date)
    estimated_completion = db.Column(db.Date)
    completion_status = db.Column(db.String())
    total_price = db.Column(db.Float)
    assigned_hours = db.Column(db.Integer)

    quote_id = db.Column(db.Integer, db.ForeignKey('quote_id'), unique=True, nullable=True)
    quote = db.relationship('Quote', back_populates='job', uselist=False)

    employee_id = db.Column(db.Integer, db.ForeignKey('employee_id'))
    employee = db.relationship('Employee', back_populates='employees', cascade='all')


class JobSchema(ma.Schema):
    employee = fields.Nested('EmployeeSchema', only=['employee_name'])
    class Meta:
        fields = ('job_id', 'estimated_start', 'estimated_completion', 'completion_status',
                  'total_price', 'assigned_hours', 'quote_id', 'employee_id', 'employee')


job_schema = JobSchema()
jobs_schema = JobSchema(many=True)