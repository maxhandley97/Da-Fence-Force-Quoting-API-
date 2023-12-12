from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from models.scopes import ScopeSchema, Scope

scopes = Blueprint('scopes', __name__, url_prefix='/scopes')

# Get all scopes
@scopes.route("/")
@jwt_required()
def all_scopes():
    # select * from scopes;
    stmt = db.select(
        Scope
    )  # .where(db.or_(Scope.status != 'Done', Scope.id > 2)).order_by(Scope.title.desc())
    scopes = db.session.scalars(stmt).all()
    return ScopeSchema(many=True, exclude=['clent.scopes']).dump(scopes)

# Get one scope
@scopes.route('/<int:id>')
@jwt_required()
def one_scope(id):
    stmt = db.select(Scope).filter_by(id=id) # .where(Scope.id == id)
    scope = db.session.scalar(stmt)
    if scope:
        return ScopeSchema().dump(scope)
    else:
        return {'error': 'Scope not found'}, 404

# Create a new scope
@scopes.route('/', methods=['POST'])
@jwt_required()
def create_scope():
    scope_info = ScopeSchema(exclude=['id', 'date_created']).load(request.json)
    scope = Scope(
        need = scope_info['need'],
        images_url = scope_info.get('images_url', ''),
        status = scope_info.get('status', 'To Do'),
        fence_type = scope_info.get('fence_type', ''),
        fence_height_mm=scope_info.get('fence_height_mm', ''),
        approximate_length_m=scope_info.get('approximate_length_mm', ''),
        client_id = get_jwt_identity()
    )
    db.session.add(scope)
    db.session.commit()
    return ScopeSchema().dump(scope), 201

# Update a scope
@scopes.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_scope(id):
    scope_info = ScopeSchema(exclude=['id', 'date_created']).load(request.json)
    stmt = db.select(Scope).filter_by(id=id) # .where(Scope.id == id)
    scope = db.session.scalar(stmt)
    if scope:
        scope.title = scope_info.get('title', scope.title)
        scope.description = scope_info.get('description', scope.description)
        scope.status = scope_info.get('status', scope.status)
        db.session.commit()
        return ScopeSchema().dump(scope)
    else:
        return {'error': 'Scope not found'}, 404

# Delete a scope
@scopes.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_scope(id):
    stmt = db.select(Scope).filter_by(id=id) # .where(Scope.id == id)
    scope = db.session.scalar(stmt)
    if scope:
        db.session.delete(scope)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Scope not found'}, 404