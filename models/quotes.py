from main import db, ma
from marshmallow import fields

class Quote(db.Model):
    __tablename__ = 'quotes'
    quote_id = db.Column(db.Integer, primary_key=True)
    fence_type = db.Column(db.String())
    price = db.Column(db.String())
    status = db.Column(db.String())
    date_posted = db.Column(db.Date)
    quote_request_id = db.Column(db.Integer, db.ForeignKey('quote_requests.id'), nullable=False)
    quote_request = db.relationship("QuoteRequest", back_populates = "quotes", cascade = "all")

    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    business = db.relationship("Business", back_populates="quotes", cascade="all, delete")

    # job = db.relationship('Job', uselist=False, back_populates='quote')

class QuoteSchema(ma.Schema):
    business = fields.Nested('BusinessSchema', only=['business_name'])
    quote_request = fields.Nested('QuoteRequestSchema', only=['id'])  # Change 'quote_request_id' to 'id'

    class Meta:
        fields = ('quote_id', 'fence_type', 'status', 'date_posted', 'quote_request', 'business_id', 'business')

quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)

    # job = fields.Nested('JobSchema', exclude=('quote',), dump_only=True)
    # barters = fields.Nested('BarterSchema', exclude=('quote',), many=True)