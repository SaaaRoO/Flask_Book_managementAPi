from infrastructure.db import db, Book, Member

class BookRepository:
    def add_book(self, book):
        db.session.add(book)
        db.session.commit()

    def get_all_books(self):
        return Book.query.all()

    def get_book_by_id(self, book_id):
        return Book.query.get(book_id)

    def update_book(self, book):
        db.session.commit()

    def delete_book(self, book):
        db.session.delete(book)
        db.session.commit()
