from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from models.quotes import QuoteSchema, Quote
from models.quote_requests import QuoteRequest, QuoteRequestSchema
from models.jobs import Job
from auth import authorised_client, check_business_id, manager_business_access, get_business_id, manager_business_client_access
from datetime import date
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

quotes = Blueprint("quotes", __name__, url_prefix="/<int:quote_request_id>/quotes")


@quotes.route("/")
@jwt_required()
@manager_business_client_access()
def all_quotes(quote_request_id):
    # select * from quote_requests;
    stmt = db.select(
        Quote
    )  # .where(db.or_(QuoteRequest.status != 'Done', QuoteRequest.id > 2)).order_by(QuoteRequest.title.desc())
    quote_requests = db.session.scalars(stmt).all()
    return QuoteSchema(many=True).dump(quote_requests)

@quotes.route("/", methods=["POST"])
@jwt_required()
@manager_business_access()
def create_quote(quote_request_id):
    try:
        business_id = get_business_id()
        logger.debug(f"business_id: {business_id}")

        # Load data from the request using QuoteSchema
        quote_info = QuoteSchema(exclude=['id', 'date_created', 'status', 'job', 'quote_request']).load(request.json)
        # Check if quote exists
        existing_request = Quote.query.filter_by(
            price=quote_info['price'],
            business_id = business_id,

        ).first()

        #ensure no duplicate
        if existing_request:
            return jsonify({"error": "You've already created this quote"}), 409

        # Create a new Quote instance
        quote = Quote(
            fence_type=quote_info.get("fence_type"),
            price=quote_info.get("price"),
            estimated_commencement=quote_info.get("estimated_commencement"),
            estimated_days_job_duration=quote_info.get("estimated_days_job_duration"),
            business_id=business_id,
            quote_request_id=quote_request_id
        )

        # Add the new quote to the database
        db.session.add(quote)
        db.session.commit()

        # Return a success message or the created quote data
        return {"message": "Quote created successfully", "Quote": QuoteSchema().dump(quote)}, 201

    except Exception as e:
        # Handle exceptions appropriately
        return {"error": str(e)}, 500


@quotes.route("/<int:quote_id>", methods=["PUT", "PATCH"])
@jwt_required()
@manager_business_access()
def update_quote(quote_request_id, quote_id):
    # Load and validate data from the request JSON using the QuoteSchema
    quote_info = QuoteSchema(exclude=["id", "date_created"]).load(request.json)
    # Select the quote from the database based on the provided quote_id
    stmt = db.select(Quote).filter_by(id=quote_id)
    quote = db.session.scalar(stmt)
    #use function to get business_id
    business_id = get_business_id(quote.business_id)
    # check if quote exists and if user is from the business
    if quote and business_id == quote.business_id:
        quote.fence_type = quote_info.get("fence_type", quote.fence_type),
        quote.price = quote_info.get("price"),
        quote.estimated_commencement = quote_info.get("estimated_commencement", quote.estimated_commencement),
        quote.estimated_days_job_duration = quote_info.get("estimated_days_job_duration", quote.estimated_days_job_duration),
        db.session.commit()
        return QuoteSchema().dump(quote)
    else:
        return {"error": "Quote not found"}, 404


# Delete a quote
@quotes.route("/<int:quote_id>", methods=["DELETE"])
@jwt_required()
def delete_quote(quote_request_id, quote_id):
    # Select the quote from the database based on the provided quote_id
    stmt = db.select(Quote).filter_by(id=quote_id)
    quote = db.session.scalar(stmt)
    if quote:
        check_business_id(quote.business_id)
        db.session.delete(quote)
        db.session.commit()
        return {}, 200
    else:
        return {"error": "Quote not found"}, 404

@quotes.route('/<int:quote_id>/accept', methods=['PUT'])
@jwt_required()
def accept_quote(quote_request_id, quote_id):
    try:
        # Get the quote request
        quote_request = QuoteRequest.query.get(quote_request_id)

        if not quote_request:
            # Handle case when the quote request does not exist
            return jsonify({"message": "Quote request not found"}), 404

        # Get the quote
        quote = Quote.query.get(quote_id)

        if not quote:
            # Handle case when the quote does not exist
            return jsonify({"message": "Quote not found"}), 404

        # Check if the quote belongs to the specified quote request
        if quote.quote_request_id != quote_request.id:
            return jsonify({"message": "Quote does not belong to the specified quote request"}), 400
        
        # Ensuring only the creator can accept the quote
        authorised_client(quote_request.client_id)

        # Change quote status to accepted
        quote.status = "accepted"

        # Create a job
        job = Job(
            estimated_start=quote.estimated_commencement,
            estimated_completion=None,
            completion_status="To Do",  # Set accordingly
            quoted_price=float(quote.price),  # Convert price to float, adjust as needed
            assigned_hours=None,  # Set accordingly
            quote_id=quote.quote_id,
            final_cost=None,
        )

        # Save changes to the database
        db.session.add(quote)
        db.session.add(job)
        db.session.commit()

        return jsonify({"message": "Quote accepted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500