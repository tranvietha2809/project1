import requests
import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

isbn = "380795272"
title = ""
author = ""
results = db.execute("""SELECT * FROM "book"
                    WHERE(isbn = :isbn OR title = :title OR author = :author)""",
                    {"isbn":isbn, "title":title, "author":author}).fetchall()
print(results)
