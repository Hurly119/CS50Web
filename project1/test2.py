import os
import csv
from flask import Flask, session, render_template, request, flash, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

key = "jKHr5blcnvzAgZ9LsNUrlg"
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# Author = "%%"
# Title = "%%"
# ISBN = "%sdfsdfsd%"
# data = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn AND title LIKE :Title AND author LIKE :Author",
# {"isbn":ISBN, "Title":Title, "Author":Author}).fetchall()
username ="Afsd"
bookISBN = "ADaf"
bookTitle = "adsada"
hasComment = db.execute("SELECT * FROM reviews WHERE username=:username AND isbn=:isbn AND title=:title",
{"username":username, "isbn":bookISBN, "title":bookTitle}).fetchall()
print(hasComment)
