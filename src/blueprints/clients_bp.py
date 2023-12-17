from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db, bcrypt
from models.clients import Client, ClientSchema, client_schema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta
from auth import authorised_client
from setup import authorised_router_error_handler


clients = Blueprint("clients", __name__, url_prefix="/clients")

@clients.route("/register", methods=["POST"])
def register_client():
    try:
        client_info = ClientSchema(exclude=["id", "is_admin"]).load(request.json)
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
@authorised_router_error_handler
def all_clients():
    authorised_client()
    stmt = db.select(
        Client
    )
    clients = db.session.scalars(stmt).all()
    return jsonify(ClientSchema(many=True, exclude=['password', 'is_admin', 'quote_requests']).dump(clients))

@clients.route("/<client_id>", methods=["DELETE"])
@jwt_required()
@authorised_router_error_handler
def delete_client(client_id):
    client = Client.query.get(client_id)
    if client:
        authorised_client(client_id)
        clientname = client.client_name
        db.session.delete(client)
        db.session.commit()
        return {"Delete": f"Success! Client {clientname} has been deleted."}, 201
    else:
        return {"error": "client not found"}, 404
    

@clients.route("/<client_id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorised_router_error_handler
def update_client(client_id):
    client_info = ClientSchema(exclude=["id", "is_admin"]).load(request.json)
    stmt = db.select(Client).filter_by(id=client_id)
    client = db.session.scalar(stmt)
    if client:
        authorised_client(client_id)
        client.client_name = client_info.get("client_name", client.client_name)
        client.email = client_info.get("email", client.email)
        client.password = client_info.get("password", client.password)
        client.phone = client_info.get("phone", client.phone)
        db.session.commit()
        return {"Update Success": f"Business {client.client_name} has been updated.", 
                "Updated Details": ClientSchema(exclude=["password"]).dump(client)}, 201
    else:
        return {"error": "client not found"}, 404



