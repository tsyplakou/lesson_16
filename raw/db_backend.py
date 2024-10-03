from .db import (
    get_library_list,
    get_library_books,
    save_book,
    add_book,
    get_book,
    get_library_books,
    get_library_name,
    get_last_book_id,
)


class DBBackend:

    @staticmethod
    def get_library_list():
        return get_library_list()

    @staticmethod
    def get_library_name(id):
        return get_library_name(id)

    @staticmethod
    def get_library_books(library_id):
        return get_library_books(library_id)

    @staticmethod
    def save_book(book):
        if book.id:
            save_book(book.id, book.library_id, book.title, book.author, book.status)
        else:
            add_book(book.title, book.author, book.status, book.library_id)
            book.id = get_last_book_id()
        # (
        #     book.id,
        #     book.library_id,
        #     book.title,
        #     book.author,
        #     book.status,
        # ) = get_book(book.id)
