from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import relationship

# Initialize the db and migrate objects
db = SQLAlchemy()
migrate = Migrate()


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, unique=True, nullable=False)
    available_copies = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "available_copies": self.available_copies
        }


class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Borrow(db.Model):
    __tablename__ = 'borrows'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, ForeignKey('books.id'), nullable=False)  # Foreign key to Book
    member_id = db.Column(db.Integer, ForeignKey('members.id'), nullable=False)  # Foreign key to Member
    borrow_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)

    # Relationship to Book and Member
    book = relationship('Book', backref='borrows')  # Book can have many borrows
    member = relationship('Member', backref='borrows')  # Member can borrow many books

    def __init__(self, book_id, member_id, borrow_date, return_date=None):
        self.book_id = book_id
        self.member_id = member_id
        self.borrow_date = borrow_date
        self.return_date = return_date

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "member_id": self.member_id,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date
        }