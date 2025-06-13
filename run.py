#!/usr/bin/env python3

from app import app, db, Hero

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if data exists
        if Hero.query.count() == 0:
            print("No data found. Running seed script...")
            from seed import seed_database
            seed_database()
        else:
            print(f"Database already contains {Hero.query.count()} heroes.")
    
    print("Starting server on http://localhost:5555")
    app.run(debug=True, port=5555)
