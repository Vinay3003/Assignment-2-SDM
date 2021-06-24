import pip
import praw
import datetime as dt
import credential
import certifi
from pymongo import MongoClient

redditAuth = praw.Reddit(client_id=credential.Client_ID, client_secret=credential.Client_SecretID, user_agent=credential.user_agent,
                         username=credential.username, password=credential.Password)

Reddit_data = []
for post in redditAuth.redditor(credential.username).submissions.top():
    redditPosts = {
        "PostId": post.id,
        "PostAuthor": post.author.name,
        "PostTitle": post.title,
        "PostText": post.selftext,
        "DateandTime": dt.datetime.fromtimestamp(post.created).strftime("%b %d %Y %H:%M:%S"),
        }
    Reddit_data.append(redditPosts)
client = MongoClient("mongodb+srv://vinayshukla3003:vinay123@socialdatamining.anz3b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFILE=certifi.where())
db = client["SDMassignment2"]
collection = db["Reddit_data"]
collection.insert_many(Reddit_data)

print(Reddit_data)