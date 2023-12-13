card_fields = card_schema.load(request.json)
    employee_id = get_jwt_identity()
    #find it in the database
    stmt = db.select(Employee).filter_by(id=employee_id)
    employee = db.session.scalar(stmt)
    if not employee:
        return abort(401, description="Invalid Employee")
    if not employee.admin: