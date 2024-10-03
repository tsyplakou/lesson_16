from sqlalchemy import Column, Integer, CHAR, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# Базовый класс для всех моделей
Base = declarative_base()

# Пример выполнения произвольного SQL-запроса
# engine.execute('ALTER TABLE users ADD COLUMN new_column VARCHAR(50)')

class Library(Base):
    __tablename__ = 'library'

    id = Column(Integer, primary_key=True)
    name = Column(CHAR(length=30), nullable=False)

    books = relationship('Book', back_populates='library')


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    author = Column(CHAR(length=50), nullable=False)
    title = Column(CHAR(length=80), nullable=False)
    status = Column(CHAR(length=8), nullable=False, default='on_shelf')
    library_id = Column(Integer, ForeignKey(Library.id), nullable=False)

    library = relationship('Library', back_populates='books')
