import requests
import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

review_input = "TESTING 123"
isbn = "553119222"
user_id = "test"
def submit_review(isbn, review_input):
    db.execute("""INSERT INTO "review" (user_id_review, isbn_review, review) VALUES
                (:user_id_review, :isbn_review, :review)""",
                {
                    "user_id_review":user_id,
                    "isbn_review": str(isbn),
                    "review" : review_input,
                })
    db.commit()

submit_review(isbn, review_input)
results = db.execute("""SELECT * FROM "review" WHERE isbn_review=:isbn""", {"isbn":isbn}).fetchone()
print(results.review)
