def authorise_client(client_id=None):
    from blueprints.clients_bp import Client
    jwt_client_id = get_jwt_identity()
    stmt = db.select(Client).filter_by(id=jwt_client_id)
    client = db.session.scalar(stmt)
    print(f"jwt_client_id: {jwt_client_id}, client_id: {client_id}")
    print(f"Client Object: {client}")
    # if its not the case that the client is an admin or client_id is truthy and matches the token
    # i.e if client_id isn"t passed in, they must be admin
    if not (client.is_admin or (client_id and jwt_client_id == client_id)):
        abort(401)