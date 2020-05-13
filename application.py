import os
import csv
from flask import Flask, session, render_template, request, flash, url_for, redirect,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import xmltodict
import json

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["DATABASE_URL"] = os.environ.get("DATABASE_URL")
app.secret_key = "egdfg"
Session(app)

key = "jKHr5blcnvzAgZ9LsNUrlg"
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    LoggedIn = "username" in session
    return render_template("index.html",LoggedIn=LoggedIn)

@app.route("/register", methods=["POST", "GET"])
def register():
    LoggedIn = "username" in session
    if request.method=="POST":
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
                    return redirect(url_for('register'))
                flash("Password does not match")
                return redirect(url_for('register'))
            flash("Account name already Taken")
            return redirect(url_for('register'))
        flash("Fields not filled.")
        return redirect(url_for('register'))
    return render_template("register.html", LoggedIn=LoggedIn)


@app.route("/login", methods=["POST", "GET"])
def login():
    LoggedIn = "username" in session
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if db.execute("SELECT * FROM users WHERE password = :password AND username = :username",
        {"password":password, "username":username}).fetchone() == None:
            flash("Log-in failed, wrong username or password")
            return redirect(url_for('login'))
        flash("Log-in successful")
        session["username"] = username
        return redirect(url_for('index'))
    return render_template("login.html", LoggedIn=LoggedIn)

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged-out")
    return redirect(url_for('login'))


@app.route("/search" , methods=["POST", "GET"])
def search():
    LoggedIn = "username" in session
    if request.method == "POST":
        ISBN = "%" + request.form.get("ISBN") +"%"
        Title = "%" +request.form.get("TITLE")+"%"
        Author = "%" +request.form.get("AUTHOR")+"%"
        bookQuery = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn AND title LIKE :Title AND author LIKE :Author",
        {"isbn":ISBN, "Title":Title, "Author":Author}).fetchall()
        if not bookQuery:
            flash("No books found")
            return redirect(url_for('search'))
        return render_template("search.html", bookQ=bookQuery, LoggedIn=LoggedIn)
    return render_template("search.html", LoggedIn=LoggedIn)

@app.route("/booksearch/<string:bookISBN>/<string:bookTitle>", methods=["POST","GET"])
def booksearch(bookISBN,bookTitle):
    LoggedIn = "username" in session
    Reviews = db.execute("SELECT * FROM reviews WHERE isbn=:isbn",
    {"isbn":bookISBN}).fetchall()
    data = requests.get("https://www.goodreads.com/search/index.xml", params={"key": "jKHr5blcnvzAgZ9LsNUrlg", "q": bookISBN})
    jsonData = json.loads(json.dumps(xmltodict.parse(data.text)))
    try:
        ReviewYear = jsonData["GoodreadsResponse"]["search"]["results"]["work"][0]
    except:
        ReviewYear = jsonData["GoodreadsResponse"]["search"]["results"]["work"]
    BookInfo = ReviewYear['best_book']
    PubYear = ReviewYear["original_publication_year"]["#text"]
    RatingsCount = int(ReviewYear["ratings_count"]["#text"])
    AVGRating = float(ReviewYear["average_rating"])
    Author = BookInfo["author"]["name"]
    Title = BookInfo["title"]
    BookIMG = BookInfo["image_url"]
    # db.execute("UPDATE books SET rateCount=:ratecount, avgRate=:avgrate WHERE title=:title",
    # {"ratecount":RatingsCount,"avgrate":AVGRating, "title":bookTitle})
    # db.commit()
    # BookDetails = db.execute("SELECT * FROM books WHERE title=:title",{"title":bookTitle})
    return render_template("booksearched.html",BookIMG=BookIMG,
    Title=Title, Author=Author,
    AVGRating=AVGRating, RatingsCount=RatingsCount, PubYear=PubYear,
    # BookDetails=BookDetails,
    LoggedIn=LoggedIn, bookISBN=bookISBN, bookTitle=bookTitle,Reviews=Reviews)

@app.route("/postreview/<string:bookISBN>/<string:bookTitle>", methods=["POST"])
def postreview(bookISBN, bookTitle):
    LoggedIn = "username" in session
    if LoggedIn:
        review = request.form.get("review")
        userRate = request.form.get("rate")
        username = session["username"]
        hasComment = db.execute("SELECT * FROM reviews WHERE username=:username AND isbn=:isbn AND title=:title",
        {"username":username, "isbn":bookISBN, "title":bookTitle}).fetchone()
        if not hasComment:
            db.execute("INSERT INTO reviews (username, review, isbn, title, rate) VALUES (:username, :review, :isbn, :title, :rate)",
            {"username":username, "review":review, "isbn":bookISBN, "title":bookTitle, "rate":userRate})
            db.commit()
            return redirect(url_for("booksearch",bookISBN=bookISBN,bookTitle=bookTitle))
        flash("Can't put more than one review")
        return redirect(url_for("booksearch",bookISBN=bookISBN,bookTitle=bookTitle))
    flash("Please log-in to review")
    return redirect(url_for("search"))

@app.route("/<string:ISBN>")
def getJson(ISBN):
    getBookDeetz = db.execute("SELECT * FROM books where isbn=:isbn",
    {"isbn":ISBN}).fetchone()
    if getBookDeetz:
        return jsonify({"title":getBookDeetz.title,"author":getBookDeetz.author,"year":getBookDeetz.year,"isbn":getBookDeetz.isbn})
    return "404"


if __name__ == "__main__":
    app.run()
