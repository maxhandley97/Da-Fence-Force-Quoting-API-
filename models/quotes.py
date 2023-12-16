from main import db, ma
from marshmallow import fields
from datetime import date

class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    fence_type = db.Column(db.String())
    price = db.Column(db.Float)
    status = db.Column(db.String())
    date_created = db.Column(db.Date)
    estimated_commencement = db.Column(db.Date, nullable=False)
    estimated_days_job_duration = db.Column(db.Integer, nullable=False)
    quote_request_id = db.Column(db.Integer, db.ForeignKey('quote_requests.id'), nullable=False)
    quote_request = db.relationship("QuoteRequest", back_populates = "quotes")

    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    business = db.relationship("Business", back_populates="quotes")

    job = db.relationship('Job', uselist=False, back_populates='quote')

class QuoteSchema(ma.Schema):
    business = fields.Nested('BusinessSchema', only=['business_name'])
    quote_request = fields.Nested('QuoteRequestSchema', only=['id']) 
    job = fields.Nested('JobSchema', only=['id']) # Change 'quote_request_id' to 'id'

    class Meta:
        fields = ('id', 'fence_type', 'status', 'date_created', 'price', 'estimated_commencement', 'estimated_days_job_duration', 'quote_request', 'business_id', 'business', 'job')

quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)

    # job = fields.Nested('JobSchema', exclude=('quote',), dump_only=True)
    # barters = fields.Nested('BarterSchema', exclude=('quote',), many=True)