from blueprints.businesses_bp import business
from blueprints.employees_bp import employees
from blueprints.quote_requests_bp import quote_requests
from blueprints.clients_bp import clients
from blueprints.jobs_bp import jobs
registerable_blueprints = [
    business,
    employees,
    clients,
    quote_requests
]