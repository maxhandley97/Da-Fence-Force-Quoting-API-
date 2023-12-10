from main import db, ma
from marshmallow import fields

class User(db.Model):
    # define the table name for the db
    __tablename__= "users"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)  
    user_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    is_manager = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)
    business = db.relationship("Business", back_populates="users")


class UserSchema(ma.Schema):
    business = fields.Nested('BusinessSchema', only=['business_name'])
    class Meta:
        fields = ('id', 'user_name', 'email', 'business', 'is_manager', 'business_id', 'is_admin', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)