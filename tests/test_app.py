import unittest
from app import create_app
from infrastructure.db import db, Book, Member


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_book(self):
        response = self.client.post('/books', json={
            'title': 'The Alchemist',
            'author': 'Paulo Coelho',
            'isbn': '1234567890123',
            'available_copies': 5
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('The Alchemist', response.get_data(as_text=True))

    def test_edit_book(self):
        with self.app.app_context():
            book = Book(title='Original Title', author='Author', isbn='1111111111111', available_copies=3)
            db.session.add(book)
            db.session.commit()

        response = self.client.put('/books/1', json={'title': 'Updated Title'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Title', response.get_data(as_text=True))

    def test_delete_book(self):
        with self.app.app_context():
            book = Book(title='To Delete', author='Author', isbn='2222222222222', available_copies=2)
            db.session.add(book)
            db.session.commit()

        response = self.client.delete('/books/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('deleted', response.get_data(as_text=True))

    def test_borrow_book(self):
        with self.app.app_context():
            book = Book(title='Borrowed Book', author='Author', isbn='3333333333333', available_copies=1)
            member = Member(name='Member One', email='member1@example.com')
            db.session.add_all([book, member])
            db.session.commit()

        response = self.client.post('/borrow', json={
            'book_id': 1,
            'member_id': 1
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('successfully borrowed', response.get_data(as_text=True))

    def test_list_borrowed_books(self):
        with self.app.app_context():
            book = Book(title='Borrowed Book', author='Author', isbn='4444444444444', available_copies=1)
            member = Member(name='Member Two', email='member2@example.com')
            borrow = Borrow(book_id=1, member_id=1, borrow_date='2024-12-22')
            db.session.add_all([book, member, borrow])
            db.session.commit()

        response = self.client.get('/members/1/borrowed')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Borrowed Book', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
