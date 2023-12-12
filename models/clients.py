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
    is_admin = db.Column(db.Boolean, default=False)

    scopes = db.relationship("Scope", back_populates="clients", cascade="all")


class ClientSchema(ma.Schema):
    scope = fields.Nested('ScopeSchema', only=['scope_id'])
    # is_manager = fields.Boolean()
    class Meta:
        fields = ('id', 'client_name', 'email', 'phone', 'password', 'scopes', 'is_admin')


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)