import sys
import os

# Adding the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from models import db, Hero, Power, HeroPower

# Creating a minimal Flask app for seeding
app = Flask(__name__)

# Using absolute path for better compatibility
db_path = os.path.abspath(os.path.join(os.getcwd(), "Superheroes", "superheroes.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def ensure_directory_exists():
    superheroes_dir = os.path.join(os.getcwd(), "Superheroes")
    if not os.path.exists(superheroes_dir):
        os.makedirs(superheroes_dir)

def seed_data():
    ensure_directory_exists()
    print(f"Using database at: {db_path}")
    with app.app_context():
        db.init_app(app)
        
        # Clearing existing data
        HeroPower.query.delete()
        Hero.query.delete()
        Power.query.delete()
        
        # Creating heroes
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra")
        ]
        
        # Creating powers
        powers = [
            Power(name="super strength", description="gives the wielder super-human strengths"),
            Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed"),
            Power(name="super human senses", description="allows the wielder to use her senses at a super-human level"),
            Power(name="elasticity", description="can stretch the human body to extreme lengths")
        ]
        
        # Adding to database
        for hero in heroes:
            db.session.add(hero)
        
        for power in powers:
            db.session.add(power)
        
        db.session.commit()
        
        # Creating hero-power relationships
        hero_powers = [
            HeroPower(strength="Strong", hero_id=1, power_id=2),
            HeroPower(strength="Average", hero_id=2, power_id=1),
            HeroPower(strength="Weak", hero_id=3, power_id=3),
        ]
        
        for hero_power in hero_powers:
            db.session.add(hero_power)
        
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
