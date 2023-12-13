from main import db, ma
from marshmallow import fields

class Client(db.Model):
    # define the table name for the db
    __tablename__= "clients"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)  
    client_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False, unique=True)
    address = db.Column(db.String(), nullable=False)
    roles = db.Column(db.String())
    is_admin = db.Column(db.Boolean, default=False)

    quote_requests = db.relationship("QuoteRequest", back_populates="client", cascade="all, delete")


class ClientSchema(ma.Schema):
    quote_requests = fields.Nested('QuoteRequestSchema', many=True, exclude=['client'])
    # manager = fields.Boolean()
    class Meta:
        fields = ('id', 'address', 'client_name', 'email', 'phone', 'password', 'quote_requests', 'is_admin', 'roles')


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)