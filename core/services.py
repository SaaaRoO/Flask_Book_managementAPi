from core.exceptions import BookNotAvailableError, MaxBorrowLimitReached


def borrow_book(member, book):
    if book.available_copies <= 0:
        raise BookNotAvailableError("No copies available.")
    if len(member.borrowed_books) >= 2:
        raise MaxBorrowLimitReached("Maximum borrow limit reached.")

    member.borrowed_books.append(book)
    book.available_copies -= 1
