from main import db, ma
from marshmallow import fields
from datetime import date

class Scope(db.Model):
    # define the table name for the db
    __tablename__= "scopes"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)  
    need = db.Column(db.String(), nullable=False)
    images_url = db.Column(db.String(), nullable=True, default=None)
    fence_type = db.Column(db.String(), nullable=True, default=None)
    fence_height_mm = db.Column(db.Integer, nullable=False)
    approximate_length_m = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.Date, default=date.today())

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    clients = db.relationship("Client", back_populates="scopes", cascade="all")


class ScopeSchema(ma.Schema):
    client = fields.Nested('ClientSchema', exclude=['is_admin', 'password'])
    # is_manager = fields.Boolean()
    class Meta:
        fields = ('id', 'need', 'images_url', 'approximate_length_m', 'fence_height_mm', 'date_created' 'clients', 'client_id')


scope_schema = ScopeSchema()
scopes_schema = ScopeSchema(many=True)

