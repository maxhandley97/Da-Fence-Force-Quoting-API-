from main import db
from flask import Blueprint
from main import bcrypt
from models.businesses import Business
from models.employees import Employee
from models.clients import Client
from models.quote_requests import QuoteRequest
# from models.jobs import Job
from models.quotes import Quote

from datetime import date, datetime

db_commands = Blueprint("db", __name__)

# create app's cli command named create, then run it in the terminal as "flask create", 
# it will invoke create_db function
# @db_commands.cli.command("drop")
# def drop_db():
#     db.drop_all()
#     print("Tables dropped") 

@db_commands.cli.command("create")
def create_db():
    db.drop_all()
    print("Tables dropped") 
    db.create_all()
    print("Tables created")

@db_commands .cli.command("seed")
def seed_db():
    businesses = [
        Business(
        business_name = "Admin",
        email = "admin@business.com",
        password = bcrypt.generate_password_hash("admin123").decode("utf-8"),
        abn = 5213125125,
        is_admin = True
    ),
    Business(
        business_name = "Max's Fencing",
        email = "max@maxsfencing.com",
        password = bcrypt.generate_password_hash("business123").decode("utf-8"),
        abn = 12345670812,
        is_admin = False
    ),
    Business(
        business_name = "Competitive Fencing",
        email = "John@competitivefencing.com",
        password = bcrypt.generate_password_hash("competitve123").decode("utf-8"),
        abn = 12345673232,
        is_admin = False
    )]
    db.session.add_all(businesses)
    db.session.commit()

    employees = [
        Employee(
            employee_name = "admin",
            email = "admin@employee.com",
            password = bcrypt.generate_password_hash("admin123456"),
            is_manager = False,
            is_admin = True,
            business_id = businesses[0].id
        ),

        Employee(
            employee_name = "Max Barbosa",
            email = "maxbarbosa@gmail.com",
            password = bcrypt.generate_password_hash("yipyipyip").decode("utf-8"),
            is_manager = True,
            is_admin = False,
            business_id = businesses[1].id
            ),
        Employee(
            employee_name = "Johnny De Fly",
            email = "jdf@gmail.com",
            password = bcrypt.generate_password_hash("jb123yipyip").decode("utf-8"),
            is_manager = False,
            is_admin = False,
            business_id = businesses[1].id
        )]
    db.session.add_all(employees)
    db.session.commit()

    clients = [
        Client(
            client_name = "admin",
            email = "admin@client.com",
            address = "22 Main Street, Mullumbimby, 2043",
            password = bcrypt.generate_password_hash("admin123456"),
            phone = "0422044123",
            is_admin = True,
        ),

        Client(
            client_name = "Jill Astron",
            email = "JA123@gmail.com",
            address = "22 Joe Street, Ocean Shores, 2043",
            password = bcrypt.generate_password_hash("jillyjill").decode("utf-8"),
            phone = "0422044333",
            ),
        Client(
            client_name = "Johnny Fermosa",
            email = "jfermosa@gmail.com",
            address = "33 Pocket Road, The Pocket, 2044",
            password = bcrypt.generate_password_hash("jf123yipyip").decode("utf-8"),
            phone = '0422044233',
        )]
    db.session.add_all(clients)
    db.session.commit()

    quote_requests = [
        QuoteRequest(
        need='Boundary Fence',
        images_url='https://example.com/image1.jpg',
        fence_type = 'Wood',
        fence_height_mm="2000",
        approximate_length_m="50",
        client_id = clients[1].id,
        date_created = datetime(2023, 11, 1)
        ),
        QuoteRequest(
        need='Pool Fence',
        images_url='https://example.com/image2.jpg',
        fence_height_mm="1200",
        approximate_length_m="40",
        client_id=clients[2].id,
        date_created = datetime(2023, 11, 12)
        ),
        QuoteRequest(
        need='Pool Fence',
        images_url='https://example.com/image3.jpg',
        fence_type = 'aluminium or glass',
        fence_height_mm="1600",
        approximate_length_m="40",
        client_id=clients[1].id,
        date_created = datetime(2023, 11, 14)
        )
        ]
    db.session.add_all(quote_requests)
    db.session.commit()

    quotes = [
        Quote(
            fence_type="aluminium",
            price = "$5,0000",
            status="Pending",
            date_posted=datetime(2023, 1, 1),
            quote_request_id = quote_requests[0].id,
            business_id = businesses[1].id
        ),
        # Add more quotes as needed
    ]
    db.session.add_all(quotes)
    db.session.commit()
                  



    # quotes_and_jobs = [
    # {
    #     'quote': Quote(
    #         fence_type="Wooden",
    #         fence_style="Lapped and Capped",
    #         fence_height_mm=1800,
    #         fence_length_m=10,
    #         images_url="https://example.com/images/quote1",
    #         status="Pending",
    #         date_posted=datetime(2023, 1, 1)
    #     ),
    #     'job': Job(
    #         estimated_start=datetime(2023, 1, 1),
    #         estimated_completion=datetime(2023, 2, 1),
    #         completion_status="Pending",
    #         total_price="1000.00",
    #         assigned_hours=20,
    #         employee_id = employees[2].id
    #     )
    # }]

    # for pair in quotes_and_jobs:
    #     db.session.add(pair['quote'])
    #     db.session.add(pair['job'])
    #     pair['job'].quote = pair['quote']

    # db.session.commit()

    # for pair in quotes_and_jobs:
    #     db.session.add(pair['quote'])
    #     db.session.add(pair['job'])
    #     pair['job'].quote = pair['quote']

    # db.session.commit()

    

    # jobs = [
    # Job(
    #     estimated_start=datetime(2023, 1, 1),
    #     estimated_completion=datetime(2023, 2, 1),
    #     completion_status="Pending",
    #     total_price="6500.00",
    #     assigned_hours=20,
    #     quote_id=1,  # Replace with actual quote_id
    #     employee_id=1  # Replace with actual employee_id
    # ),
    # # Add more jobs as needed
    # ]
    # db.session.add_all(jobs)
    # db.session.commit()

    # Seed data for Quotes
    

    # Seed data for Barters
    # barters = [
    #     Barter(
    #         post_date=datetime(2023, 1, 1),
    #         quote_id=1,  # Replace with actual quote_id
    #         employee_id=1,  # Replace with actual employee_id
    #         business_id=businesses[1].id
    #     ),
    #     # Add more barters as needed
    # ]
    # db.session.add_all(barters)
    # db.session.commit()`


    print("Table seeded") 
