from sqlalchemy import *
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pandas as pd
from .models import Book, Borrow

Base = declarative_base()

#USERNAME = 'blairlyt'
USERNAME = 'rhaenysg'


class DatabaseConnector:
    def __init__(self, username=USERNAME, host='localhost', port='5432', database=USERNAME):
        self.username = username
        self.host = host
        self.port = port
        self.database = database

    def add(self, title, author, published):
        engine = create_engine(f'postgresql://{self.username}@{self.host}:{self.port}/{self.database}')
        Session = sessionmaker(bind=engine)
        session = Session()
        book = Book(title=title, author=author, published=published, date_added=datetime.now().date().strftime('%Y-%m-%d'))
        session.add(book)
        session.commit()
        return book.book_id

    def delete(self, title, author, year):
        engine = create_engine(f'postgresql://{self.username}@{self.host}:{self.port}/{self.database}')
        Session = sessionmaker(bind=engine)
        session = Session()
        book = session.query(Book).filter(Book.title == title, Book.author == author, Book.published == year).first()
        br = session.query(Borrow).filter(Borrow.book_id == book.book_id).first()
        deletedate = datetime.now().date()
        if br == None:
            book.date_deleted = deletedate
            session.commit()
            return True
        else:
            if br.date_end != null and br.date_end < deletedate:
                book.date_deleted = deletedate
                session.commit()
                return True
            else:
                return False

    def list_books(self):
        engine = create_engine(f'postgresql://{self.username}@{self.host}:{self.port}/{self.database}')
        Session = sessionmaker(bind=engine)
        session = Session()
        books = session.query(Book.title, Book.author, Book.published, Book.date_deleted).all()
        return books

    def get_book(self, title, author, year):
        engine = create_engine(f'postgresql://{self.username}@{self.host}:{self.port}/{self.database}')
        Session = sessionmaker(bind=engine)
        session = Session()
        book = session.query(Book).filter(Book.title == title, Book.author == author, Book.published == year).first()
        return book if (book and book.date_deleted == None) else None

    def borrow(self, book_id, user_id):
        engine = create_engine(f'postgresql://{self.username}@{self.host}:{self.port}/{self.database}')
        Session = sessionmaker(bind=engine)
        session = Session()
        #borrow = session.query(Borrow).filter(Borrow.book_id == book_id, Borrow.date_end == None).first()
        borrow = Borrow(book_id=book_id, user_id=user_id, date_start=datetime.now().date())
        session.add(borrow)
        session.commit()
        return borrow.borrow_id

    def get_borrow(self, user_id):
        engine = create_engine(f'postgresql://{self.username}@{self.host}:{self.port}/{self.database}')
        Session = sessionmaker(bind=engine)
        session = Session()
        borrow = session.query(Borrow).filter(Borrow.user_id == user_id).first()
        return borrow.borrow_id if borrow else None

    def retrieve(self, borrow_id):
        engine = create_engine(f'postgresql://{self.username}@{self.host}:{self.port}/{self.database}')
        Session = sessionmaker(bind=engine)
        session = Session()
        borrow = session.query(Borrow).filter(Borrow.borrow_id == borrow_id, Borrow.date_end == None).first()
        if borrow:
            borrow.date_end = datetime.now().date()
            retrieved_book = session.query(Book.title, Book.author, Book.published).filter(Book.book_id == borrow.book_id).first()
            session.commit()
            return retrieved_book
        else:
            return None

    def book_statistics(self, book_id):
        engine = create_engine(f'postgresql://{self.username}@{self.host}:{self.port}/{self.database}')
        Session = sessionmaker(bind=engine)
        session = Session()

        query = session.query(Borrow).filter_by(book_id=book_id)
        df = pd.read_sql(query.statement, query.session.bind)
        df.drop('user_id', axis=1, inplace=True)

        return df

