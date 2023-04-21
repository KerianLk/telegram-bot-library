from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True)
    title = Column(String(255))
    author = Column(String(255))
    published = Column(String(255))
    date_added = Column(DateTime)
    date_deleted = Column(DateTime, nullable=True)

    #borrows = relationship('Borrow', back_populates='book')


class Borrow(Base):
    __tablename__ = 'borrows'

    borrow_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.book_id'))
    date_start = Column(DateTime)
    date_end = Column(DateTime, nullable=True)
    user_id = Column(Integer)

    #book = relationship('Book', back_populates='borrows')
