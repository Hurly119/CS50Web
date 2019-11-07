import os
import csv
from flask import Flask, session, render_template, request, flash, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/loginpg")
def loginpg():
    return render_template("login.html")

@app.route("/registerpg")
def registerpg():
    return render_template("register.html")

@app.route("/searchpg")
def searchpg():
    return render_template("search.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    cpass = request.form.get("cpass")
    if(username and password and cpass):
        if db.execute("SELECT * FROM users WHERE username = :username",
        {"username":username}).fetchone() == None:
            if password == cpass:
                db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                {"username":username, "password":password})
                db.commit()
                flash("Register successful")
                return redirect(url_for('registerpg'))
            flash("Password does not match")
            return redirect(url_for('registerpg'))
    flash("Account name already taken; Fields not filled.")
    return redirect(url_for('registerpg'))

@app.route("/login", methods=["POST","GET"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if db.execute("SELECT * FROM users WHERE password = :password AND username = :username",
    {"password":password, "username":username}).fetchone() == None:
        flash("Log-in failed, wrong username or password")
        return redirect(url_for('loginpg'))
    flash("Log-in successful")
    return redirect(url_for('index'))


@app.route("/search" , methods=["POST"])
def search():
    ISBN = "%" + request.form.get("ISBN") +"%"
    Title = "%" +request.form.get("TITLE")+"%"
    Author = "%" +request.form.get("AUTHOR")+"%"
    bookQ = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn AND title LIKE :Title AND author LIKE :Author",
    {"isbn":ISBN, "Title":Title, "Author":Author}).fetchall()
    if bookQ == None:
        flash("No books found")
        return redirect(url_for('searchpg'))
    return render_template("search.html", bookQ=bookQ)
