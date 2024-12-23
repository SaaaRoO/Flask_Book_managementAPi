# Book Management API

This project provides a Flask-based RESTful API for managing books and borrowing records. It is designed using clean architecture principles and implements the repository pattern for better separation of concerns and maintainability.

## Features
- Add, edit, delete, and retrieve books.
- Maintain a record of borrowed books.
- Implements validation for unique fields like ISBN.
- Handles errors gracefully with meaningful responses.

## Setup Instructions

### Prerequisites
- Python 3.9 or later
- SQLite (or another database, with modifications to `db_setup.py`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/book-management-api.git
   cd book-management-api

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Configure environment variables (optional):
* Create a .env file in the root directory.
* Add database configuration:
   ```bash
   DATABASE_URL=sqlite:///db.sqlite3

5. Initialize the database:
   ```bash
   python -m infrastructure.db_setup

6. Run the application:
   ```bash 
   flask run

7. Open your browser and navigate to:
   ```bash
   http://127.0.0.1:5000/Swagger

## Testing the API

* Use a tool like Postman or cURL or Swagger to interact with the following endpoints:

* Endpoints

- GET /api/books - Retrieve all books.

- GET /api/books/<book_id> - Retrieve a book by ID.

- POST /api/books - Add a new book.

- PUT /api/books/<book_id> - Update book details.

- DELETE /api/books/<book_id> - Delete a book.

* Error Handling

- Returns 400 Bad Request for validation errors (e.g., duplicate ISBN).

- Returns 404 Not Found for non-existent resources.

- Returns 500 Internal Server Error for unexpected issues.

* Future Enhancements

- Add user authentication and authorization.

- Implement borrowing history with due dates and penalties.

- Support for other database backends like PostgreSQL or MySQL.


* Contributing

- Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.


