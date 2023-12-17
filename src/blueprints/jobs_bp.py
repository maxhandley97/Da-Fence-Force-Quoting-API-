from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from main import db
from models.jobs import Job, JobSchema
from models.jobs import Job
from datetime import date
from setup import authorised_router_error_handler
from auth import get_business_id, authorised_business_or_manager
from sqlalchemy.exc import IntegrityError


jobs = Blueprint("jobs", __name__, url_prefix="/<int:business_id>/jobs")

@jobs.route("/")
@authorised_router_error_handler
@jwt_required()
def all_jobs(business_id):
    jwt_identity = get_jwt_identity()
    if jwt_identity is None:
        abort(401, description="JWT identity not found")

    id = get_business_id()
    if id == business_id:
        stmt = db.select(Job).filter_by(business_id=business_id)
        jobs = db.session.scalars(stmt).all()
        return JobSchema(many=True).dump(jobs)
    else:
        abort(401, description="invalid token")



# Update a job
@jobs.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_job(id):
    job_info = JobSchema(exclude=['id', 'date_created']).load(request.json)
    stmt = db.select(Job).filter_by(id=id) 
    job = db.session.scalar(stmt)
    business_id = get_business_id(job.business_id)
    if job and business_id == job.business_id:
        job.estimated_completion = job_info.get('estimated_completion', job.estimated_completion)
        job.description = job_info.get('description', job.description)
        job.images_url = job_info.get('images_url', job.images_url)
        job.fence_type = job_info.get('fence_type', job.fence_type)
        job.fence_height_mm = job_info.get('fence_height_mm', job.fence_height_mm)
        job.approximated_length_m = job.get('approximated_length_m', job.approximated_length_m)
        db.session.commit()
        return JobSchema().dump(job)
    else:
        return {'error': 'JobRequest not found'}, 404
