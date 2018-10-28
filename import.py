import os
import psycopg2
import csv

#Check if database URL exists
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("Error: Database url not set")

#connect to Database
db_url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(db_url)
if not connection:
    raise RuntimeError("Could not connect to database")

#Create book table in Database
cursor = connection.cursor()
cursor.execute("""
    DROP TABLE book
    """)
cursor.execute("""
    CREATE TABLE book(
        id SERIAL,
        isbn VARCHAR NOT NULL PRIMARY KEY,
        title VARCHAR NOT NULL,
        author VARCHAR NOT NULL,
        year INTEGER NOT NULL
        )""")
connection.commit()

#Read CSV data
filep = open("books.csv", "r")
if not filep:
    raise RuntimeError("Error open CSV file")
reader = csv.reader(filep)
next(reader) #skip header
#cursor.copy_from(filep, 'book', sep = ",") - cannot recognize comma between names
for row in reader:
    print("Inserting row: {}".format(row))
    cursor.execute(
        "INSERT INTO book (isbn, title, author, year) VALUES (%s, %s, %s, %s)", row
        )
connection.commit()
