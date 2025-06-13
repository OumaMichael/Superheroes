from app import app, db
from seed import seed_database

if __name__ == '__main__':
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        # Run the seed file
        seed_database()
