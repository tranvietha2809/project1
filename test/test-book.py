import requests
import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
book_info = db.execute("""SELECT user_id_review, isbn, title, author, year, review FROM book
                INNER JOIN review ON book.isbn = review.isbn_review
                WHERE user_id_review= :user_id_review AND isbn=:isbn""",
                {"user_id_review" : "test", "isbn" : "553119222"}).fetchone()

print(book_info.isbn)
