def test_add_book(client):
    response = client.post('/api/books', json={
        "title": "Sample Book",
        "author": "Author Name",
        "isbn": "1234567890",
        "available_copies": 5
    })
    assert response.status_code == 201
