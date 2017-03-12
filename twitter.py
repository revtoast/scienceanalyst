import ignore
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from twitterdata_to_json import *
from tweepy import Stream
from tweepy.streaming import StreamListener


# ----------------------------------------------#
#                                               #
#     define the user account to be serialized  #
#     - all of the following functions          #
#     are defined in twitterdata_to_json.py     #
#                                               #
#-----------------------------------------------#
user = "PacktPub"



#gathers the maximum amount of tweets (3200?) from the users feed and
#serializes it as a jsonl file (every line is a "json file")

# user_timeline_to_jsonl(user)

#searches the jsonl file for '#' followed by letters and/or numbers and adds
#them to a pandas dataframe for fast

# search_hashtags_in_jsonl(user)

#-----------------------------------------------#
#                                               #
#     define the hashtags to look for           #
#     using the search API                      #
#                                               #
#-----------------------------------------------#


#works but super slow - needs optimization
search_hashtags = ['science']
hashtagcount = 0

class hashtagcounter(StreamListener):

    def on_data(self, data):
        global hashtagcount
        hashtagcount += 1
        print (hashtagcount)
        return(True)

    def on_error(self, status):
        print('Error!')


auth = twitter_authentication()

Sciencecounter = Stream(auth, hashtagcounter())
Sciencecounter.filter(track=search_hashtags)




#-----------------------------------------------#
#                                               #
#     create the output we use for graphs etc   #
#                                               #
#-----------------------------------------------#
def create_hashtag_usage_dataframe(user):
    hashoccurence = {}
    hashliste = search_hashtags_in_jsonl(user)
    for item in hashliste:
        hashoccurence[item] = hashliste.count(item)

    df = pd.DataFrame()
    df['hashtag'] = hashoccurence.keys()
    df['count'] = hashoccurence.values()
    df = df.sort_values(['count'], ascending=False)
    return df


# print(create_hashtag_usage_dataframe(user))
