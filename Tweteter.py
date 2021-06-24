import tweepy as tw
import credential
import certifi
from pymongo import MongoClient


auth = tw.OAuthHandler(credential.API_key, credential.API_secretkey)
auth.set_access_token(credential.Access_token, credential.Accesss_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

tweets = api.user_timeline(screen_name="@vinaysh68493686", count=100, include_rts=False, tweet_mode='extended')
tweetsData = []
for info in tweets:
    status = {
        "ID": str(info.id), "TweetAuthor": info.author.name,
        "TweetText": info.full_text, "DateandTime": info.created_at.strftime("%b %d %Y %H:%M:%S"),
        "TweetSource": info.source
    }
    tweetsData.append(status)
client = MongoClient(
    "mongodb+srv://vinayshukla3003:vinay123@socialdatamining.anz3b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFILE=certifi.where())
db = client["Socialdatamining"]
collection = db["Tweeter_data"]
collection.insert_many(tweetsData)
print(tweetsData)