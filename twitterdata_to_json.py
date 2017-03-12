#from twitterauthentication import *
import ignore
import json
import os
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor
import re

hashliste = []

def twitter_authentication():
  #returns twitter OAuthHandler object
    try:
      #authentication keys have been defined via environment variables in the unix OS
      #for now these are saved in another py file to not be uploaded to version control
      consumer_key = ignore.TWITTER_CONSUMER_KEY
      consumer_secret = ignore.TWITTER_CONSUMER_SECRET
      access_token = ignore.TWITTER_ACCESS_TOKEN
      access_secret = ignore.TWITTER_ACCESS_SECRET
    except KeyError:
      sys.stderr.write("TWITTER_* environment variables not set\n")
      sys.exit(1)

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

def twitter_login_client():
    auth = twitter_authentication()
    client = API(auth)
    return client


def user_timeline_to_jsonl(user):
    client = twitter_login_client()
    userFile = 'user_time-line_{}.jsonl'.format(user)

    with open (userFile, 'w') as f:
        for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(16):
            for status in page:
                f.write(json.dumps(status._json)+"\n")
    f.close()

#search_hashtags_in_jsonl(user) function could be improved by using "entities" -> which is a dictionary of
#urls, hashtags and mentions in the tweet (jsonl feature!)
'''
"entities": {
    "hashtags": [
      {
        "indices": [
          72,
          79
        ],
        "text": "Python" <- this is the hashtag embedded in the tweet
      }
    ]
'''
def search_hashtags_in_jsonl(user):
    userFile = 'user_time-line_{}.jsonl'.format(user)

    with open (userFile, 'r') as f:
        for line in f:
            liste = re.findall(r"#[a-z0-9A-Z]+", str(json.loads(line))) #finds all hash signs followed by letters or numbers

            for item in liste:
                item = return_umlaute(item)
                hashliste.append(item)

    return hashliste

def return_umlaute(item):
    item = item.replace('\xe4', 'ae') #replaces ä
    item = item.replace('\xc4', 'Ae') #replaces Ä
    item = item.replace('\xf6', 'oe') #replaces ö
    item = item.replace('\xd6', 'Oe') #replaces Ö
    item = item.replace('\xfc', 'ue') #replaces ü
    item = item.replace('\xdc', 'Ue') #replaces Ü
    return item
