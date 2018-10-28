import os

from utils import *
from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError
from passlib.hash import sha256_crypt


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Check API key
if not os.getenv("API_KEY"):
    raise RuntimeError("API_KEY not set")
api_key = os.getenv("API_KEY")

@app.route("/")
@login_required
def index():
    return render_template('main.html', user_id = session["user_id"])

@app.route("/search", methods = ["POST"])
@login_required
def search():
    isbn = request.form.get("isbn")
    title = request.form.get("book_title")
    author = request.form.get("author")
    results = db.execute("""SELECT * FROM "book"
                        WHERE(isbn = :isbn OR title = :title OR author = :author)""",
                        {"isbn":isbn, "title":title, "author":author}).fetchall()
    db.commit()
    return render_template('results.html', results= results)

@app.route("/login", methods = ["GET", "POST"])
def login():
    #clear all user_id
    session.clear()
    #if user submit form from index
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        results = db.execute("""SELECT * FROM "user"
                            WHERE (user_id = :username)""",
                            {"username":username}).fetchone()

        #ensure username exist and password is matched
        if not results or sha256_crypt.verify(password, results[2]) != True :
            return render_template("login.html")

        #remember which user is logged in
        session["user_id"] = results[1]
        db.commit()
        return redirect(url_for("index"))

    #if user access login through URL
    else:
        return render_template("login.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    #if user submit register form
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password confirmation")

    #if username is blank
    #    if not username:
    #        return render_template("apology.html",
    #            message = "Please enter username!")

    #if password is blank
    #    if not password:
    #        return render_template("apology.html",
    #            message = "Please enter password!")

    #if password confirmation do not match
    #    if password != password_confirm:
    #        return render_template("apology.html",
    #        message = "Password and password confirmation don't match")

    #inserting user into database
        password = sha256_crypt.encrypt(password)
        try:
            db.execute("""INSERT INTO "user" (user_id, password)
                        VALUES (:user_id, :password)""",
                        {"user_id": username, "password": password})
        except IntegrityError:
            return render_template("apology.html",
                message = "Username already taken!")
        db.commit()
        return render_template("register_success.html")

    #if user access via URL
    elif request.method == "GET":
        return render_template("register.html")

@app.route("/book/<isbn>")
def book(isbn):
    book_info = db.execute("""SELECT isbn, title, author, year FROM book
                                WHERE isbn= :isbn""", {"isbn":str(isbn)}).fetchone()
    user_info = db.execute("""SELECT review, user_id_review FROM review
                    WHERE user_id_review= :user_id_review AND isbn_review=:isbn""",
                    {"user_id_review":session["user_id"], "isbn":str(isbn)}).fetchone()
    if not user_info:
        review = None;
    else:
        review = user_info.review
    db.commit()
    return render_template("book.html", book_info = book_info, review = review)


@app.route("/submit_review")
def submit_review():
    review_input = request.form.get("my_review")
    return redirect(url_for("book"))

@app.route("/sign_out")
def logout():
    session.clear()
    return redirect(url_for("index"))
