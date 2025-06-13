# Superhero API - Challenge 2

A Flask REST API for managing superheroes and their powers, built to match the provided Postman collection requirements.

## Features

- **Heroes Management**: List heroes and get individual hero details with powers
- **Powers Management**: List powers, get individual powers, and update power descriptions
- **Hero-Power Relationships**: Create relationships between heroes and powers
- **Data Validation**: Robust validation for all inputs
- **RESTful Design**: Follows REST conventions

## Database Schema

The application uses three main models:

- **Hero**: Stores hero information (id, name, super_name)
- **Power**: Stores power information (id, name, description)
- **HeroPower**: Junction table linking heroes to powers with strength levels

## API Endpoints (Matching Postman Collection)

### 1. GET /heroes
Returns a list of all heroes with basic information.

**Response Format:**
\`\`\`json
[
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  }
]
\`\`\`

### 2. GET /heroes/<int:id>
Returns detailed information about a specific hero including their powers.

**Response Format:**
\`\`\`json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
    {
      "id": 1,
      "hero_id": 1,
      "power_id": 2,
      "strength": "Strong",
      "power": {
        "id": 2,
        "name": "flight",
        "description": "gives the wielder the ability to fly through the skies at supersonic speed"
      }
    }
  ]
}
\`\`\`

### 3. GET /powers
Returns a list of all powers.

**Response Format:**
\`\`\`json
[
  {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  }
]
\`\`\`

### 4. GET /powers/<int:id>
Returns detailed information about a specific power.

**Response Format:**
\`\`\`json
{
  "id": 1,
  "name": "super strength",
  "description": "gives the wielder super-human strengths"
}
\`\`\`

### 5. PATCH /powers/<int:id>
Updates a power's description.

**Request Body:**
\`\`\`json
{
  "description": "Valid Updated Description"
}
\`\`\`

**Response Format:**
\`\`\`json
{
  "id": 1,
  "name": "super strength",
  "description": "Valid Updated Description"
}
\`\`\`

### 6. POST /hero_powers
Creates a new hero-power relationship.

**Request Body:**
\`\`\`json
{
  "strength": "Average",
  "power_id": 1,
  "hero_id": 3
}
\`\`\`

**Response Format:**
\`\`\`json
{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Average",
  "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
  },
  "power": {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  }
}
\`\`\`

## Setup Instructions

1. **Clone the repository**
   \`\`\`bash
   git clone <repository-url>
   cd superhero-api
   \`\`\`

2. **Create virtual environment**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Run the application**
   \`\`\`bash
   python run.py
   \`\`\`

The API will be available at `http://localhost:5555`

## Testing with Postman

1. Import the provided `challenge-2-superheroes.postman_collection.json` file into Postman
2. The collection contains all 6 required endpoints
3. Run the requests to test the API functionality

## Testing with Python Scripts

Run the test scripts to verify functionality:

\`\`\`bash
# Test all Postman collection endpoints
python test_postman_endpoints.py

# Test validation scenarios
python test_validation.py
\`\`\`

## Validation Rules

- **HeroPower strength**: Must be one of 'Strong', 'Weak', or 'Average'
- **Power description**: Must be present and at least 20 characters long
- **Hero and Power**: Must exist when creating relationships

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- `404` for not found resources
- `400` for validation errors with `{"errors": ["validation errors"]}`
- `500` for server errors

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database

## Project Structure

\`\`\`
superhero-api/
├── app.py                    # Main application with models
├── routes.py                 # API routes
├── seed.py                   # Database seeding
├── run.py                    # Application runner
├── test_postman_endpoints.py # Postman collection tests
├── test_validation.py        # Validation tests
├── requirements.txt          # Dependencies
└── README.md                # This file
\`\`\`

## Author

[Your Name]

## License

This project is licensed under the MIT License.
