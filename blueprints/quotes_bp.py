from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from models.quotes import QuoteSchema, Quote
from models.employees import Employee
from models.businesses import Business
from auth import roles_required
from decorators import client_or_business_required

quotes = Blueprint("quotes", __name__, url_prefix="/<int:quote_request_id>/quotes")


@quotes.route("/")
@jwt_required()
@client_or_business_required('business', 'employee_manager', 'admin', 'client')
def all_quotes(quote_request_id):
    # select * from quote_requests;
    stmt = db.select(
        Quote
    )  # .where(db.or_(QuoteRequest.status != 'Done', QuoteRequest.id > 2)).order_by(QuoteRequest.title.desc())
    quote_requests = db.session.scalars(stmt).all()
    return QuoteSchema(many=True).dump(quote_requests)

@quotes.route("/", methods=["POST"])
@jwt_required()
@roles_required('business', 'employee_manager', 'admin')
def create_quote(quote_request_id):
    try:
        # Extract user identity from the JWT
        user_id = get_jwt_identity()

        # Try to find the employee in the database
        employee = Employee.query.get(user_id)

        if employee:
            # If the user is an employee, use their business_id
            business_id = employee.business_id
        else:
            # If the user is not an employee, try to find the business in the database
            business = Business.query.get(user_id)

            if not business:
                # If neither employee nor business found, return an error
                return {"error": "User not found or not authorized"}, 401

            # If the user is a business, use their business_id
            business_id = business.id

        # Load data from the request using QuoteSchema
        quote_info = QuoteSchema(exclude=['id', 'date_created', 'status', 'job', 'quote_request']).load(request.json)

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
        return {"message": "Quote created successfully"}, 201

    except Exception as e:
        # Handle exceptions appropriately
        return {"error": str(e)}, 500



@quotes.route("/<int:quote_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_quote(quote_request_id, quote_id):
    quote_info = QuoteSchema(only=["message"]).load(request.json)
    stmt = db.select(Quote).filter_by(id=quote_id)  # .where(Quote.id == id)
    quote = db.session.scalar(stmt)
    if quote:
        quote.message = quote_info.get("message", quote.message)
        db.session.commit()
        return QuoteSchema().dump(quote)
    else:
        return {"error": "Quote not found"}, 404


# Delete a quote
# DELETE /quote_requests/<quote_request_id>/quotes/<quote_id>
@quotes.route("/<int:quote_id>", methods=["DELETE"])
@jwt_required()
def delete_quote(quote_request_id, quote_id):
    stmt = db.select(Quote).filter_by(id=quote_id)  # .where(Quote.id == id)
    quote = db.session.scalar(stmt)
    if quote:
        authorize(quote.user_id)
        db.session.delete(quote)
        db.session.commit()
        return {}, 200
    else:
        return {"error": "Quote not found"}, 404
