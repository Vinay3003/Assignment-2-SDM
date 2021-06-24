from flask import Flask, request, render_template
from pymongo import MongoClient
import credential
import tweepy as tw
import datetime as dt
import praw
import certifi

app = Flask(__name__)

# mongodb connection
client = MongoClient(
    "mongodb+srv://vinayshukla3003:vinay123@socialdatamining.anz3b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFILE=certifi.where())
db = client.Socialdatamining

# reddit authentication
redditAuth = praw.Reddit(client_id=credential.Client_ID, client_secret=credential.Client_SecretID, user_agent=credential.user_agent,
                         username=credential.username, password=credential.Password)

# twitter authentication
auth = tw.OAuthHandler(credential.API_key, credential.API_secretkey)
auth.set_access_token(credential.Access_token, credential.Accesss_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

@app.route('/')
def shows():
    return render_template('main.html')

@app.route('/Reddit')
def Reddit():
    return render_template("Reddit.html")

@app.route('/Twitter')
def Twitter():
    return render_template("Twitter.html")

@app.route('/redditUpdate', methods=['POST'])
def redditUpdate():
    title = request.values.get("title")
    status = request.values.get("status")
    sub = redditAuth.subreddit("u_Vinayat3003")
    update = sub.submit(title, status)
    collection = db.Reddit_data
    collection.insert_one({
        "PostId": update.id,
        "PostAuthor": update.author.name,
        "PostTitle": update.title,
        "PostText": update.selftext,
        "Dateandtime": dt.datetime.fromtimestamp(update.created).strftime("%b %d %Y %H:%M:%S"),
    })
    return render_template('main.html')

@app.route('/twitterUpdate', methods=['POST'])
def twitterUpdate():
    tweet = request.values.get("status")
    update = api.update_status(tweet)
    collection = db.Tweeter_data
    collection.insert_one({
        "ID": str(update.id),
        "TweetAuthor": update.author.name,
        "TweetText": update.text,
        "DateandTime": update.created_at.strftime("%b %d %Y %H:%M:%S"),
        "TweetSource": update.source
    })
    return render_template('main.html')

if __name__ == '__main__':
    app.debug = True
    app.run()