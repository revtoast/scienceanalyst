import base64
from get_bearer_token import *
import ignore
import json
import requests
import datetime
import time


#in order to only get minutious file names we set the second and microsecond
#in the datetime object to 0
d = str(datetime.datetime.now().replace(second=0, microsecond=0))


#this specifies the date 7 days back in order to retrieve tweets that were posted within the last 3 days
today = datetime.date.today() + datetime.timedelta(days=1)
lastweek = today - datetime.timedelta(days=3)


#to receive a bearer token for OAuth2 authentication
#this method can be called - once a token is generated the method will
#always return this one until it is invalidated/invalid
#bearer_token = get_bearer_token(consumer_key, consumer_secret)


# ----------------------------------------------#
#                                               #
#     define the search query to be serialized  #
#     as well as some global variables          #
#                                               #
#-----------------------------------------------#
query ='%23ICURehab'
data_dictionary = {}
newestID = 0
# SEARCH API info: https://dev.twitter.com/rest/public/search
# %23 = # / %40 = @
# for multiple query arguments either append the string with a + or create a list and
# link the list elements with a + (for example %23kekstortenauflauf+%23wurstbrotkonfetti)
# function for replacing @/# with the respective %-symbols will follow in order to
# make the application web compatible


def super_fast_hashtag_query(query, oldestID = 0):
    #global variables used in the function as well as the OAuth2 token
    global newestID
    global data_dictionary
    bearer_token = ignore.BEARER_TOKEN

    # these variables can be printed for debugging
    #print("lastid: {}".format(oldestID))
    #print("neuID: {}".format(newestID))

    #in case of the first run of this function, we look for the most recent tweets
    #with our specified query keywords (usually only 100 tweets are returned
    # - to be safe we set the receivable count to 1000)
    if oldestID == 0:
        url = 'https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=recent&since={}&until={}&count=1000'.format(query, lastweek, today)
        # this can be used in order to switch between writing(w) and appending(a) of files
        #schreibtyp = 'w'

    #when the function is called recursively the oldestID now is the starting point for the new query
    #with the same keywords as before
    else:
        url = 'https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=recent&max_id={}&count=1000'.format(query, oldestID)
        #schreibtyp = 'a'

    #accessing the twitterAPI page requires us to provide a bearer_token which is send
    #via headers in the request (we use the requests library for the url-handling)
    headers = {'Authorization': 'Bearer '+ bearer_token + '', 'User-Agent': 'science analysis client'}
    r = requests.get(url, headers=headers)

    #the result(r) that we get from twitter is a json file (basically one large dictionary)
    #which we reformat using the json library and subsequently create a list (testliste)
    #which contains all dictionary fields within the 'statuses' dictionary values
    tweet_dictionary = json.loads(r.text)
    testliste = [tweet_dictionary['statuses']]

    #since the resulting list (testliste) is a list of dictionaries we iterate
    #through the items of the lists and choose the appropriate values to store
    #in our data_dictionary
    for items in testliste:
        for item in items:
            # this condition checks if the query reached the last available
            # entry which means that the str_id of the status and the max_id
            # of the search_metadata are the same and there already is an
            # entry in the dictionary with the tweetID
            if newestID == oldestID and newestID in data_dictionary.keys():
                print("done")
                return data_dictionary

            # in case of different newest and oldest IDs we have a list of unique
            # tweets to add to our "database" and now use the tweetID as keys
            # and the relevant information as a list of values

            # !!!! we still need to implement äöüß and other special character      !!!!
            # !!!! transformation in order to have "normal" text in the text fields !!!!
            else:
                ts = time.strftime('%Y-%m-%d %H:%M', time.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                data_dictionary[item["id_str"]] = [ts, item['user']['id_str'], item['user']['screen_name'], item['retweet_count'], str(item['text'].encode('UTF-8'))[2:-1]]
                oldestID = items[len(items)-1]['id_str']

        #this is the last ID of the query -> timepoint 0 from which we go backwards 7-10 days
        newestID = str(tweet_dictionary['search_metadata']['max_id'])

        #using the oldest ID we start a new twitter SEARCH API query and append it to the data_dictionary
        super_fast_hashtag_query(query, oldestID)


#call of the function in order to fill the data_dictionary with tweets
super_fast_hashtag_query(query)
#we print the length of the dictionary for debugging purposes
print (len(data_dictionary))


#for key, value in data_dictionary.items():
#    print (key, value)

# **************      for the DF we need      ************** #
# - time or tweetID as index
# - hashtags
# - userID
# - tweettext


#still needs to be implemented
def replace_non_ascii(query):
    print(query)
