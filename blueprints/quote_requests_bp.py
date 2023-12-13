from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from models.quote_requests import QuoteRequestSchema, QuoteRequest, quote_requests_schema
from blueprints.quotes_bp import quotes
from decorators import client_or_business_required
from datetime import date
from auth import authorise_client

quote_requests = Blueprint('quote_requests', __name__, url_prefix='/quote_requests')

quote_requests.register_blueprint(quotes)

@quote_requests.route("/")
@jwt_required()
@client_or_business_required('business_owner', 'employee_manager', 'admin', 'client')
def all_quote_requests():
    # select * from quote_requests;
    stmt = db.select(
        QuoteRequest
    )  # .where(db.or_(QuoteRequest.status != 'Done', QuoteRequest.id > 2)).order_by(QuoteRequest.title.desc())
    quote_requests = db.session.scalars(stmt).all()
    return QuoteRequestSchema(many=True).dump(quote_requests)
    
# Get one quote_request
@quote_requests.route('/<int:id>')
@jwt_required()
@client_or_business_required('business_owner', 'employee_manager', 'admin', 'client')
def one_quote_request(id):
    stmt = db.select(QuoteRequest).filter_by(id=id) # .where(QuoteRequest.id == id)
    quote_request = db.session.scalar(stmt)
    if quote_request:
        return QuoteRequestSchema().dump(quote_request)
    else:
        return {'error': 'QuoteRequest not found'}, 404

# Create a new quote_request
@quote_requests.route('/', methods=['POST'])
@jwt_required()
def create_quote_request():
    jwt_client_id = get_jwt_identity()
    quote_request_info = QuoteRequestSchema(exclude=['id', 'date_created']).load(request.json)
    # Check if request exists
    existing_request = QuoteRequest.query.filter_by(
        need=quote_request_info['need'],
        client_id=jwt_client_id,
        date_created=quote_request_info.get('date_created', date.today())
    ).first()
    
    #ensure no duplicate
    if existing_request:
        return jsonify({"error": "You've already created this quote request"}), 409
    
    quote_request = QuoteRequest(
    need=quote_request_info['need'],
    images_url=quote_request_info.get('images_url', ''),
    status=quote_request_info.get('status', ''),
    fence_type=quote_request_info.get('fence_type', ''),
    fence_height_mm=quote_request_info.get('fence_height_mm', ''),  # Set default value to None
    approximate_length_m=quote_request_info.get('approximate_length_mm', ''),  # Set default value to None
    client_id=jwt_client_id
)
    db.session.add(quote_request)
    db.session.commit()
    return QuoteRequestSchema().dump(quote_request), 201


# Update a quote_request
@quote_requests.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_quote_request(id):
    quote_request_info = QuoteRequestSchema(exclude=['id', 'date_created']).load(request.json)
    stmt = db.select(QuoteRequest).filter_by(id=id) # .where(QuoteRequest.id == id)
    quote_request = db.session.scalar(stmt)
    if quote_request:
        quote_request.title = quote_request_info.get('title', quote_request.title)
        quote_request.description = quote_request_info.get('description', quote_request.description)
        quote_request.status = quote_request_info.get('status', quote_request.status)
        db.session.commit()
        return QuoteRequestSchema().dump(quote_request)
    else:
        return {'error': 'QuoteRequest not found'}, 404

# Delete a quote_request
@quote_requests.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_quote_request(id):
    stmt = db.select(QuoteRequest).filter_by(id=id) # .where(QuoteRequest.id == id)
    quote_request = db.session.scalar(stmt)
    if quote_request:
        db.session.delete(quote_request)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'QuoteRequest not found'}, 404
    


# Get one quote_request
# @quote_requests.route('/<int:id>/accept_quote')
# @jwt_required()
# def accept_quote(quote_request_id, quote_id):
#     # Get the quote request
#     # get the quote
#     # change quote status to accepted
#     # create job

    