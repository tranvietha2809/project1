import requests
import os

from utils import *
from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
username = "test"
password = "123"
user = db.execute("""SELECT * from "user" WHERE user_id=:user_id""",{"user_id" : username}).fetchone()
print(user.user_id)
