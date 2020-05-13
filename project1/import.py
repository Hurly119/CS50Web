import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
ISBN = '038435';
Title = None;
Author = None;
bookQ = db.execute("SELECT title FROM books WHERE isbn LIKE :isbn AND title LIKE :Title AND author LIKE :Author",
{"isbn":ISBN, "Title":Title, "Author":Author})
for x in bookQ:
    print((x))
print(bookQ == None)
# books = open("books.csv")
# read = csv.reader(books)
# for isbn,title,author,year in read:
#     db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
#                   {"isbn":isbn, "title":title, "author":author, "year":year})
# db.commit()
