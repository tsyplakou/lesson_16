from .db import get_session

from .tables import (
    Book,
    Library,
)


class DBBackend:

    @staticmethod
    def get_library_list():
        with get_session() as session:
            return [
                (library.id, library.name)
                for library in session.query(Library).all()
            ]

    @staticmethod
    def get_library_name(id):
        with get_session() as session:
            return session.query(Library).get(id).name

    @staticmethod
    def get_library_books(library_id):
        with get_session() as session:
            return [
                (
                    book.id,
                    book.library_id,
                    book.title,
                    book.author,
                    book.status,
                ) for book in session.query(Book).filter_by(
                    library_id=library_id,
                )
            ]

    @staticmethod
    def save_book(book):
        with get_session() as session:
            if book.id:
                session.query(Book).filter_by(id=book.id).update(dict(
                    library_id=book.library_id,
                    title=book.title,
                    author=book.author,
                    status=book.status,
                ))
            else:
                book_db = Book(
                    library_id=book.library_id,
                    title=book.title,
                    author=book.author,
                    status=book.status,
                )
                session.add(book_db)
            session.commit()
