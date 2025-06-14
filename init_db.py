import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from models import db

# Create a minimal Flask app for database initialization
app = Flask(__name__)

# Use absolute path for better compatibility
db_path = os.path.abspath(os.path.join(os.getcwd(), "Superheroes", "superheroes.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def ensure_directory_exists():
    superheroes_dir = os.path.join(os.getcwd(), "Superheroes")
    if not os.path.exists(superheroes_dir):
        os.makedirs(superheroes_dir)
        print(f"Created Superheroes directory at: {superheroes_dir}")

def init_database():
    ensure_directory_exists()
    print(f"Database will be created at: {db_path}")
    with app.app_context():
        db.init_app(app)
        db.create_all()
        print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()
