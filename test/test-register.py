import requests
import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
username = "vhax"
password = "x123"
db.execute("""INSERT INTO "user" (user_id, password) VALUES (:user_id, :password)""",{"user_id" : username, "password" : password})
db.commit()
