import os
import psycopg2

#Check if database URL exists
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("Error: Database url not set")

#connect to Database
db_url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(db_url)
if not connection:
    raise RuntimeError("Could not connect to database")

#Create user table in Database
cursor = connection.cursor()
cursor.execute(""" DROP TABLE "user";""")
cursor.execute("""
    CREATE TABLE "user"(
        id SERIAL,
        user_id VARCHAR NOT NULL PRIMARY KEY,
        password VARCHAR NOT NULL
        );""")
connection.commit()

cursor.execute("""
    CREATE TABLE "review"(
        review_id SERIAL PRIMARY KEY,
        user_id_review VARCHAR REFERENCES "user"(user_id),
        isbn_review VARCHAR REFERENCES "book"(isbn),
        review VARCHAR
    );""")
connection.commit()
