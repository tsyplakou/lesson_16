from .constants import DB_CONNECTION
from .db_connect import DBConnect

db = DBConnect(**DB_CONNECTION)


def _add_cursor_wrapper(func):
    def wrapper(*args, **kwargs):
        with db.get_connection().cursor() as cur:
            return func(cur, *args, **kwargs)

    return wrapper


@_add_cursor_wrapper
def get_library_books(cur, library_id):
    cur.execute(
        '''
        SELECT id, library_id, title, author, status FROM book
        WHERE library_id = %s
        ''',
        (library_id,)
    )
    return cur.fetchall()


@_add_cursor_wrapper
def get_book(cur, id):
    cur.execute(
        '''
        SELECT id, library_id, title, author, status FROM book
        WHERE id = %s
        ''',
        (id,)
    )
    return cur.fetchone()


@_add_cursor_wrapper
def get_library_list(cur):
    cur.execute(
        '''
        SELECT id, name FROM libraries
        order by id
        ''',
        ()
    )
    return cur.fetchall()


@_add_cursor_wrapper
def save_book(cur, id, library_id, title, author, status):
    cur.execute(
        f'''
        UPDATE book
        SET library_id = %s, title = %s, author = %s, status = %s
        WHERE id = %s
        ''',
        (library_id, title, author, status, id)
    )


@_add_cursor_wrapper
def add_book(cur, title, author, status, library_id):
    cur.execute(
        f'''
        INSERT INTO book (title, author, status, library_id)
        VALUES (%s, %s, %s, %s)
        ''',
        (title, author, status, library_id)
    )



@_add_cursor_wrapper
def get_library_name(cur, id):
    cur.execute(
        '''
        SELECT name FROM libraries
        WHERE id = %s
        ''',
        (id,)
    )
    return cur.fetchone()[0]


@_add_cursor_wrapper
def get_last_book_id(cur):
    cur.execute(
        '''
        SELECT MAX(id) FROM book
        ''',
        ()
    )
    return cur.fetchone()[0]
