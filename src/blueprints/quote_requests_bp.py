from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from main import db
from models.quote_requests import QuoteRequestSchema, QuoteRequest, quote_requests_schema
from models.jobs import Job
from models.quotes import Quote
from blueprints.quotes_bp import quotes
from datetime import date
from auth import authorised_client, manager_business_client_access
from setup import authorised_router_error_handler

quote_requests = Blueprint('quote_requests', __name__, url_prefix='/quote_requests')

quote_requests.register_blueprint(quotes)

@quote_requests.route("/")
@jwt_required()
@manager_business_client_access()
@authorised_router_error_handler
def all_quote_requests():
    # select * from quote_requests;
    stmt = db.select(
        QuoteRequest
    )  # .where(db.or_(QuoteRequest.status != 'Done', QuoteRequest.id > 2)).order_by(QuoteRequest.title.desc())
    quote_requests = db.session.scalars(stmt).all()
    return jsonify(QuoteRequestSchema(many=True).dump(quote_requests))

@quote_requests.route("client/<int:client_id>")
@jwt_required()
@manager_business_client_access()
@authorised_router_error_handler
def quote_requests_by_client(client_id=None):
    # Fetch quote requests for the specified client
    stmt = db.select(QuoteRequest).where(QuoteRequest.client_id == client_id)
    quote_requests = db.session.scalars(stmt).all()

    return QuoteRequestSchema(many=True).dump(quote_requests)

# Get one quote_request
@quote_requests.route('/<int:id>')
@jwt_required()
@manager_business_client_access()
@authorised_router_error_handler
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
@authorised_router_error_handler
@manager_business_client_access()
def create_quote_request():
    #must verify if client
    verify_jwt_in_request()
    jwt_client_id = get_jwt_identity()
    claims = get_jwt()
    if claims.get("roles") == "client":
        pass
    else:
        abort(401)
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
@authorised_router_error_handler
def update_quote_request(id):
    quote_request_info = QuoteRequestSchema(exclude=['id', 'date_created']).load(request.json)
    stmt = db.select(QuoteRequest).filter_by(id=id) 
    quote_request = db.session.scalar(stmt)
    if quote_request:
        authorised_client(quote_request.client_id)
        quote_request.need = quote_request_info.get('need', quote_request.need)
        quote_request.description = quote_request_info.get('description', quote_request.description)
        quote_request.images_url = quote_request_info.get('images_url', quote_request.images_url)
        quote_request.fence_type = quote_request_info.get('fence_type', quote_request.fence_type)
        quote_request.fence_height_mm = quote_request_info.get('fence_height_mm', quote_request.fence_height_mm)
        quote_request.approximate_length_m = quote_request_info.get('approximate_length_m', quote_request.approximate_length_m)
        db.session.commit()
        return QuoteRequestSchema().dump(quote_request)
    else:
        return {'error': 'QuoteRequest not found'}, 404

# Delete a quote_request
@quote_requests.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorised_router_error_handler
def delete_quote_request(id):
    stmt = db.select(QuoteRequest).filter_by(id=id) # .where(QuoteRequest.id == id)
    quote_request = db.session.scalar(stmt)
    if quote_request:
        db.session.delete(quote_request)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'QuoteRequest not found'}, 404
    

# @quote_requests.route('/<int:quote_request_id>/<int:quote_id>/accept', methods=['PUT'])
# @jwt_required()
# def accept_quote(quote_request_id, quote_id):
#     try:
#         # Get the quote request
#         quote_request = QuoteRequest.query.get(quote_request_id)

#         if not quote_request:
#             # Handle case when the quote request does not exist
#             return jsonify({"message": "Quote request not found"}), 404

#         # Get the quote
#         quote = Quote.query.get(quote_id)

#         if not quote:
#             # Handle case when the quote does not exist
#             return jsonify({"message": "Quote not found"}), 404

#         # Check if the quote belongs to the specified quote request
#         if quote.quote_request_id != quote_request.id:
#             return jsonify({"message": "Quote does not belong to the specified quote request"}), 400
        
#         # Ensuring only the creator can accept the quote
#         authorised_client(quote_request.client_id)

#         # Change quote status to accepted
#         quote.status = "accepted"

#         # Create a job
#         job = Job(
#             estimated_start=quote.estimated_commencement,
#             estimated_completion=None,
#             completion_status="To Do",  # Set accordingly
#             quoted_price=float(quote.price),  # Convert price to float, adjust as needed
#             assigned_hours=None,  # Set accordingly
#             quote_id=quote.quote_id,
#             final_cost=None,
#         )

#         # Save changes to the database
#         db.session.add(quote)
#         db.session.add(job)
#         db.session.commit()

#         # Return success message
#         return jsonify({"message": "Quote accepted"}), 200

#     except Exception as e:
#         # Handle exceptions appropriately
#         return jsonify({"error": str(e)}), 500
