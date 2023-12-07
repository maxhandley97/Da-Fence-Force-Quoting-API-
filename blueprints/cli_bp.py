from main import db
from flask import Blueprint
from main import bcrypt
from models.businesses import Business
from models.users import User

from datetime import date

db_commands = Blueprint("db", __name__)

# create app's cli command named create, then run it in the terminal as "flask create", 
# it will invoke create_db function
@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 

@db_commands.cli.command("create")
def create_db():
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
    )]
    db.session.add_all(businesses)
    db.session.commit()
    users = [
        User(
            user_name = "admin",
            email = "admin@admin.com",
            password = bcrypt.generate_password_hash("admin123456"),
            is_manager = False,
            is_client = False,
            is_admin = True,
            business_id = businesses[0].id
        ),

        User(
            user_name = "Max Barbosa",
            email = "maxbarbosa@gmail.com",
            password = bcrypt.generate_password_hash("yipyipyip").decode("utf-8"),
            is_manager = True,
            is_client = False,
            is_admin = False,
            business_id = businesses[1].id
            ),
        User(
            user_name = "Johnny De Fly",
            email = "jdf@gmail.com",
            password = bcrypt.generate_password_hash("jb123yipyip").decode("utf-8"),
            is_manager = False,
            is_client = False,
            is_admin = False,
            business_id = businesses[1].id
        )]
    db.session.add_all(users)
    db.session.commit()


    print("Table seeded") 
