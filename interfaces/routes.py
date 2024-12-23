from flask import Blueprint, request, jsonify
from application.book_service import (
    add_book,
    edit_book,
    delete_book,
    get_all_books,
    get_book_by_id,
    borrow_book_service
)
from infrastructure.db import db, Book, Member

def register_routes(app):
    api = Blueprint('api', __name__)

    # Add a new book
    @api.route('/books', methods=['POST'])
    def create_book():
        data = request.json
        book = add_book(data)
        return jsonify({"id": book.id, "title": book.title}), 201

    # Edit a book by ID
    @api.route('/books/<int:book_id>', methods=['PUT'])
    def edit_book_endpoint(book_id):
        data = request.json
        book = edit_book(book_id, data)
        if not book:
            return jsonify({"error": "Book not found"}), 404
        return jsonify({"message": "Book updated successfully", "book": book}), 200

    # Delete a book by ID
    @api.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book_endpoint(book_id):
        success = delete_book(book_id)
        if not success:
            return jsonify({"error": "Book not found"}), 404
        return jsonify({"message": "Book deleted successfully"}), 200

    # Get all books
    @api.route('/book_management_api/All_books', methods=['GET'])
    def get_books():
        books = Book.query.all()
        return jsonify([book.to_dict() for book in books])

    # Get a book by ID
    @api.route('/books/<int:book_id>', methods=['GET'])
    def get_book(book_id):
        book = Book.query.get(book_id)
        if book:
            return jsonify(book.to_dict())
        return jsonify({"error": "Book not found"}), 404

    # Borrow a book
    @api.route('/books/<int:book_id>/borrow', methods=['POST'])
    def borrow_book_endpoint(book_id):
        data = request.json
        member_name = data.get('member_name')
        
        if not member_name:
            return jsonify({"error": "Member name is required"}), 400
        
        # Lookup or create member
        member = Member.query.filter_by(name=member_name).first()
        if not member:
            member = Member(name=member_name)
            db.session.add(member)
            db.session.commit()

        # Ensure the book is available for borrowing
        book = Book.query.get(book_id)
        if not book or book.available_copies <= 0:
            return jsonify({"error": "Book not available"}), 400

        # Borrow the book (update available copies, etc.)
        book.available_copies -= 1
        db.session.commit()

        return jsonify({"message": "Book borrowed successfully"}), 200

    app.register_blueprint(api, url_prefix='/api')
