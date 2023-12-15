def authorised_manager(employee_id=None):
    from blueprints.employees_bp import Employee
    jwt_employee_id = get_jwt_identity()
    
    stmt = db.select(Employee).filter_by(id=employee_id)
    employee = db.session.scalar(stmt)
    
    if not (employee.is_admin or (employee_id and jwt_employee_id == employee_id)):
        abort(401, description="You are not an authorised employee.")
