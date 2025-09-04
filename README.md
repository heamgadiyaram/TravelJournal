# Travel Journal API


A RESTful service that allows users to manage their travel experiences. Users can create, read, update, and delete journal entries, each containing a destination, visit date, optional notes, and optional rating.

The API is built using Python, Flask, and PyMySQL, with a MySQL database backend.

### Key Features
- CRUD operations for travel entries
- Input validation, including date-only and rating checks
- JSON API responses with clear success/error messages
- Modular code design with separation of concerns

## Technologies Used
- Python 3: Backend language, familiar and flexible
- Flask: Lightweight web framework for REST API
- PyMySQL: Direct MySQL connection without ORM
- MySQL: Relational database for structured travel data
- Postman: API testing and development
- Flask Blueprints: Modular routing for scalable endpoints

## Database Design
Table: `travels`
- id: INT, primary key, auto-increment
- destination: string, required
- visit_date: date (YYYY-MM-DD), required
- notes: string, optional
- rating: float (0.0 to 10.0), optional

## API Endpoints

### Base URL
`/api/travel-journal`

### Create Entry
- POST `/api/travel-journal/entry`
- Required: destination, visit_date (YYYY-MM-DD)
- Optional: notes, rating (0.0–10.0)
- Success (201): `{"message": "Travel created successfully."}`
- Error (400): `{"error": "Description of validation error"}`

### Get All Entries
- GET `/api/travel-journal/entries`
- Success (200): Returns list of all entries, empty list if none

### Get Single Entry
- GET `/api/travel-journal/entry/<id>`
- Success (200): Returns JSON of specific entry
- Error (404): `{"error": "Travel not found"}`

### Update Entry
- PUT `/api/travel-journal/entry/<id>`
- JSON: Any combination of destination, visit_date, notes, rating
- Success (200): `{"message": "Record updated successfully."}`
- Errors:
  - `{"error": "Travel not found"}`
  - `{"error": "visit_date must be in YYYY-MM-DD format"}`

### Delete Entry
- DELETE `/api/travel-journal/entry/<id>`
- Success (200): `{"message": "Travel record deleted"}`
- Error (404): `{"error": "Travel not found"}`

### Create Photo
- GET `/api/travel-journal/entry/<id>/photo`
- Success (200): `{"destination": destination, "image_url": image_url,}`
- Error (!200): `{"error": "could not find image for destination"}`
- Error (404): `{"message": "No image found for this destination"}`



