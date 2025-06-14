# Superheroes API

A Flask REST API for managing superheroes and their powers.

## Features

- CRUD operations for heroes and powers
- Many-to-many relationship between heroes and powers
- Data validation for power descriptions and hero-power strength levels
- JSON API responses
- SQLite database with SQLAlchemy ORM

## Setup Instructions

1. Clone this repository
2. Create a virtual environment:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Initialize the database:
   \`\`\`bash
   python init_db.py
   \`\`\`

5. Seed the database with sample data:
   \`\`\`bash
   python seed.py
   \`\`\`

6. Run the application:
   \`\`\`bash
   python app.py
   \`\`\`

The API will be available at `http://localhost:5555`

## API Endpoints

- `GET /heroes` - Get all heroes
- `GET /heroes/<id>` - Get a specific hero with their powers
- `GET /powers` - Get all powers
- `GET /powers/<id>` - Get a specific power
- `PATCH /powers/<id>` - Update a power's description
- `POST /hero_powers` - Create a new hero-power relationship

## Database Schema

The application uses three main models:
- **Hero**: Represents a superhero with name and super_name
- **Power**: Represents a superpower with name and description
- **HeroPower**: Junction table linking heroes to powers with strength level

## Validations

- Power descriptions must be at least 20 characters long
- HeroPower strength must be one of: 'Strong', 'Weak', 'Average'


## Testing the API with Postman

You can use [Postman](https://www.postman.com/) to interact with the API endpoints. Here’s how to test creating and updating resources:

### Example: Creating a Power

1. **Set the request method:** `POST`
2. **Set the URL:** `http://localhost:5555/powers`
3. **Go to the Body tab:**  
  - Select **raw**
  - Choose **JSON** as the format
  - Paste the following JSON:
  ```json
  {
    "name": "super strength",
    "description": "gives the wielder incredible physical strength beyond normal human limits"
  }
  ```

### Example: Creating a Hero

- **POST** `http://localhost:5555/heroes`
- Body:
  ```json
  {
   "name": "Peter Parker",
   "super_name": "Spider-Man"
  }
  ```

### Example: Creating a HeroPower Relationship

- **POST** `http://localhost:5555/hero_powers`
- Body:
  ```json
  {
   "strength": "Strong",
   "hero_id": 1,
   "power_id": 1
  }
  ```

### Example: Updating a Power

- **PATCH** `http://localhost:5555/powers/1`
- Body:
  ```json
  {
   "description": "Updated description that is much longer than twenty characters to meet requirements"
  }
  ```

> **Note:** The app uses `force=True` to parse JSON, so requests will work even if the `Content-Type` header is not set to `application/json`.

