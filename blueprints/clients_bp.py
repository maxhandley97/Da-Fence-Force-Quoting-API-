from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db, bcrypt
from models.clients import Client, ClientSchema, client_schema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta
from auth import authorised_client


clients = Blueprint("clients", __name__, url_prefix="/clients")

@clients.route("/register", methods=["POST"])
def register_client():
    try:
        client_info = ClientSchema(exclude=["id", "is_admin", ""]).load(request.json)
        client = Client(
            client_name = client_info["client_name"],
            email = client_info["email"],
            password = bcrypt.generate_password_hash(client_info["password"]).decode("utf8"),
            address = client_info["address"],
            phone = client_info["phone"]
        )
        db.session.add(client)
        db.session.commit()
        return ClientSchema(exclude=["password"]).dump(client), 201

    except IntegrityError:
        return {"error": "Client already signed up"}, 409
    
@clients.route("/login/", methods=["POST"])
def login_as_client():
    client_info = ClientSchema(only=["email", "password"]).load(request.json)
    stmt = db.select(Client).where(Client.email == client_info["email"])
    client = db.session.scalar(stmt)
    if client and bcrypt.check_password_hash(client.password, client_info["password"]):
        additional_claims = {"roles": "client"}
        token = create_access_token(identity=client.id, expires_delta=timedelta(weeks=2), additional_claims = additional_claims)
        return {"status": "successful login", "token": token, "client": ClientSchema(exclude=["password", "is_admin", "quote_requests"]).dump(client)}
    else:
        return {"error": "Invalid email or password"}, 401

# Get all clients
@clients.route("/")
@jwt_required()
def all_clients():
    authorised_client()
    stmt = db.select(
        Client
    )  # .where(db.or_(Card.status != "Done", Card.id > 2)).order_by(Card.title.desc())
    clients = db.session.scalars(stmt).all()
    return ClientSchema(many=True, exclude=['password', 'is_admin', 'address', 'phone']).dump(clients)

@clients.route("/<client_id>", methods=["DELETE"])
@jwt_required()
def delete_client(client_id):
    authorised_client(client_id)
    # Parse incoming POST body through schema
    client = Client.query.get(client_id)
    if client:
        clientname = client.client_name
        db.session.delete(client)
        db.session.commit()
        return {"Delete": f"Success! Client {clientname} has been deleted."}, 201
    else:
        return {"error": "client not found"}, 404




