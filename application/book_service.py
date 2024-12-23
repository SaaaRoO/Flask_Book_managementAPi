from pkgutil import get_data
from sqlite3 import IntegrityError

from flask import jsonify, request
from infrastructure.db import Borrow, db, Book, Member
from datetime import datetime

def add_book(data):
    book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn'],
        available_copies=data['available_copies']
    )
    db.session.add(book)
    db.session.commit()
    return book

from infrastructure.db import db, Book

def edit_book(book_id, data):
    book = get_book_by_id(book_id)
    if not book:
        raise ValueError("Book not found")
    
    # Update book fields
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.isbn = data.get('isbn', book.isbn)
    book.available_copies = data.get('available_copies', book.available_copies)
    
    # Validate ISBN uniqueness
    existing_book = db.session.query(Book).filter(Book.isbn == book.isbn, Book.id != book_id).first()
    if existing_book:
        raise ValueError("ISBN already exists for another book")
    
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError("Failed to update book. Ensure all fields are valid.")
    
    return book

def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return False
    db.session.delete(book)
    db.session.commit()
    return True


def get_all_books():
    books = Book.query.all()
    return [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "available_copies": book.available_copies
        }
        for book in books
    ]

def get_book_by_id(book_id):
    book = Book.query.get(book_id)
    if not book:
        return None
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "available_copies": book.available_copies
    }

def borrow_book_service(member, book_id):
    book = Book.query.get(book_id)
    if book and book.available_copies > 0:
        # Create a new Borrow record
        borrow = Borrow(book_id=book.id, member_id=member.id, borrow_date=datetime.now())
        db.session.add(borrow)
        db.session.commit()

        # Update available copies of the book
        book.available_copies -= 1
        db.session.commit()
        
        return borrow
    else:
        return None