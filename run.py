import math
import os

from orm import DBBackend
# from raw import DBBackend


def clear_console():
    os.system('clear')


def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


class Book:
    STATUS_ON_SHELF = 'on_shelf'
    STATUS_ON_HANDS = 'on_hands'

    def __init__(self, id, library_id, author, title, status):
        self.id = id
        self.library_id = library_id
        self.author = author
        self.title = title
        self.status = status

    @classmethod
    def create_book(cls, library_id, author, title, status):
        book = cls(None, library_id, author, title, status)
        book.save()
        return book

    def set_on_hands(self):
        self.status = self.STATUS_ON_HANDS
        self.save()

    def set_on_shelf(self):
        self.status = self.STATUS_ON_SHELF
        self.save()

    def save(self):
        DBBackend.save_book(self)

    def __str__(self):
        return (
            f'{self.title} by {self.author}'
            f' status: {self.status}'
        )


class Library:
    BOOKS_PER_SHELF = 7

    def __init__(self, id):
        self.id = id
        self.name = DBBackend.get_library_name(id)
        self.books = [
            Book(*data) for data in
            DBBackend.get_library_books(id)
        ]

    def take_book_by_title(self, title):
        try:
            book = next(filter(
                lambda book: book.title == title,
                self.books
            ))
            book.set_on_hands()
        except StopIteration:
            print(f'Book "{title}" not found')

    def take_book_by_number(self, number):
        try:
            book = self.books_on_shelf[number - 1]
            book.set_on_hands()
        except IndexError:
            print(f'Book "{number}" not found')

    def return_book_by_number(self, number):
        try:
            book = self.books_on_hands[number - 1]
            book.set_on_shelf()
        except IndexError:
            print(f'Book "{number}" not found')

    @property
    def books_on_shelf(self):
        return [
            book
            for book in self.books
            if book.status == Book.STATUS_ON_SHELF
        ]

    @property
    def books_on_hands(self):
        return [
            book
            for book in self.books
            if book.status == Book.STATUS_ON_HANDS
        ]

    def draw_bookshelf(self):
        clear_console()
        books_on_shelf = self.books_on_shelf

        for book_shelf_nr in range(math.ceil(len(books_on_shelf) / self.BOOKS_PER_SHELF)):
            shelf_width = len(books_on_shelf[
                book_shelf_nr * self.BOOKS_PER_SHELF:
                (book_shelf_nr + 1) * self.BOOKS_PER_SHELF
            ])
            shelf_offset = book_shelf_nr * self.BOOKS_PER_SHELF
            print(f'__{"_____" * shelf_width}__')
            print('| ', '  _  ' * shelf_width, ' |', sep='')
            print(
                '| ',
                *[
                    f' |{books_on_shelf[book_nr + shelf_offset].author[0]}| '
                    for book_nr in range(shelf_width)
                ],
                ' |',
                sep='',
            )
            print(
                '| ',
                *[
                    f' |{books_on_shelf[book_nr + shelf_offset].title[0]}| '
                    for book_nr in range(shelf_width)
                ],
                ' |',
                sep='',
            )
            print('| ', '  ‾  ' * shelf_width, ' |', sep='')
            print(f'‾‾{"‾‾‾‾‾" * shelf_width}‾‾')


class LibraryManager:
    def __init__(self):
        self.library = None

    def set_library(self, library_id):
        self.library = Library(library_id)

    def _draw_menu(self):
        print(
            '0. Select library\n'
            '1. Take a book by title\n'
            '2. Take a book by number\n'
            '3. Return book by number\n'
            '4. Add new book\n'
            '5. List books on shelf\n'
            '6. List books on hands\n'
            '7. Draw shelf\n'
            '8. Let\'s play\n'
            '-1. Exit\n'
        )

    def run_operation(self):
        while True:
            self._draw_menu()
            choice = input('Choose an operation: ')

            match choice:
                case '0':
                    print(*[
                        '{}. {}'.format(*data)
                        for data in DBBackend.get_library_list()
                    ], sep='\n')
                    self.set_library(input('Enter library ID: '))
                case '1':
                    title = input('Enter book title: ')
                    self.library.take_book_by_title(title)
                case '2':
                    for nr, book in enumerate(self.library.books_on_shelf, start=1):
                        print(f'{nr}. ', book)
                    number = read_int('Enter book number: ')
                    self.library.take_book_by_number(number)
                case '3':
                    for nr, book in enumerate(self.library.books_on_hands, start=1):
                        print(f'{nr}. ', book)
                    number = read_int('Enter book number: ')
                    self.library.return_book_by_number(number)
                case '4':
                    title = input('Enter book title: ')
                    author = input('Enter book author: ')
                    print(*DBBackend.get_library_list(), sep='\n')
                    library_id = read_int('Enter book library ID: ')
                    self.library.books.append(
                        Book.create_book(library_id, title, author, Book.STATUS_ON_SHELF)
                    )
                    print('Book added successfully')
                case '5':
                    for book in self.library.books_on_shelf:
                        print(book)
                case '6':
                    for book in self.library.books_on_hands:
                        print(book)
                case '7':
                    self.library.draw_bookshelf()
                case '8':
                    breakpoint()
                case '-1':
                    return


def library_controller():
    LibraryManager().run_operation()


if __name__ == "__main__":
    library_controller()
    # from raw.db import get_library_list, get_library_books
    # breakpoint()
