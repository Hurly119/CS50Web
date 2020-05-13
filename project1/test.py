import requests
import xmltodict
import json
data = requests.get("https://www.goodreads.com/search/index.xml", params={"key": "jKHr5blcnvzAgZ9LsNUrlg", "q":"Under The Tuscan Sun"})
jsonData = json.loads(json.dumps(xmltodict.parse(data.text)))
# ReviewYear = jsonData["GoodreadsResponse"]["search"]["results"]["work"][0]
# BookInfo = ReviewYear['best_book']
# PubDate = ReviewYear["original_publication_month"]["#text"]+"/"+ReviewYear["original_publication_day"]["#text"]+"/"+ReviewYear["original_publication_year"]["#text"]
# RatingsCount = int(ReviewYear["ratings_count"]["#text"])
# AVGRating = float(ReviewYear["average_rating"])
# Author = BookInfo["author"]["name"]
# Title = BookInfo["title"]
# BookIMG = BookInfo["image_url"]
print(jsonData)
