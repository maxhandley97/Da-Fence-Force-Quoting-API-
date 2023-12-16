from main import db, ma
from marshmallow import fields
from datetime import date

class QuoteRequest(db.Model):
    # define the table name for the db
    __tablename__= "quote_requests"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)  
    need = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    images_url = db.Column(db.String(), nullable=True)
    fence_type = db.Column(db.String(), nullable=True)
    fence_height_mm = db.Column(db.String(), nullable=True)
    approximate_length_m = db.Column(db.String(), nullable=True)
    date_created = db.Column(db.Date, default=date.today())
    status = db.Column(db.String(), default="To Do")

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    client = db.relationship("Client", back_populates="quote_requests", cascade="all, delete")

    quotes = db.relationship("Quote", back_populates="quote_request", cascade="all, delete")


class QuoteRequestSchema(ma.Schema):
    client = fields.Nested('ClientSchema', exclude=['is_admin', 'password', 'quote_requests', 'roles'])
    quotes = fields.Nested('QuoteSchema', many=True, exclude=['quote_request'])

    class Meta:
        fields = ('id', 'need', 'description', 'images_url', 'fence_type', 'status',
                   'approximate_length_m', 'fence_height_mm', 'date_created', 'client', 'client_id', 'quotes')


quote_request_schema = QuoteRequestSchema()
quote_requests_schema = QuoteRequestSchema(many=True)

