from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from models.quotes import QuoteSchema, Quote
# from auth import authorize
from decorators import client_or_business_required

quotes = Blueprint("quotes", __name__, url_prefix="/<int:quote_request_id>/quotes")


@quotes.route("/")
@jwt_required()
@client_or_business_required('business_owner', 'employee_manager', 'admin', 'client')
def all_quotes(quote_request_id):
    # select * from quote_requests;
    stmt = db.select(
        Quote
    )  # .where(db.or_(QuoteRequest.status != 'Done', QuoteRequest.id > 2)).order_by(QuoteRequest.title.desc())
    quote_requests = db.session.scalars(stmt).all()
    return QuoteSchema(many=True).dump(quote_requests)

@quotes.route("/", methods=["POST"])
@jwt_required()
@client_or_business_required('business_owner', 'employee_manager', 'admin', 'client')
def create_quote(quote_request_id):
    quote_info = QuoteSchema(only=["message"]).load(request.json)
    quote = Quote(
        message=quote_info["message"], user_id=get_jwt_identity(), quote_request_id=quote_request_id
    )
    db.session.add(quote)
    db.session.commit()
    return QuoteSchema().dump(quote), 201

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
