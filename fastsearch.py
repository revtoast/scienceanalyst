import base64
import ignore
import json
import requests
import datetime

consumer_key = ignore.TWITTER_CONSUMER_KEY
consumer_secret = ignore.TWITTER_CONSUMER_SECRET
access_token = ignore.TWITTER_ACCESS_TOKEN
access_secret = ignore.TWITTER_ACCESS_SECRET

#in order to only get minutious file names we set the second and microsecond
#in the datetime to 0
d = str(datetime.datetime.now().replace(second=0, microsecond=0))


#in order to receive a bearer token for OAuth2 authentication
#this method can be called - once a token is generated the method will
#always return this one until it is invalidated/invalid
def get_bearer_token(consumer_key, consumer_secret):
    # get bearer token for application only requests
    bearer_token_credentials = base64.urlsafe_b64encode('{}:{}'.format(consumer_key, consumer_secret).encode('ascii')).decode('ascii')
    url = 'https://api.twitter.com/oauth2/token'
    headers = {
    'Authorization': 'Basic {}'.format(bearer_token_credentials),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }
    data = 'grant_type=client_credentials'
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    if response_data['token_type'] == 'bearer':
        bearer_token = response_data['access_token']
    else:
        raise RuntimeError('unexpected token type: {}'.format(response_data['token_type']))
    return bearer_token


#bearer_token = get_bearer_token(consumer_key, consumer_secret)



# SEARCH API info: https://dev.twitter.com/rest/public/search
# %23 = # / %40 = @
# for multiple query arguments either append the string with a + or create a list and
# link the list elements with a + (for example %23kekstortenauflauf+%23wurstbrotkonfetti)
# function for replacing @/# with the respective %-symbols will follow in order to
# make the application web compatible
query ='%23science'

def replace_non_ascii(query):
    print(query)


def super_fast_hashtag_query(query):
    bearer_token = ignore.BEARER_TOKEN
    url = 'https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query)
    headers = {'Authorization': 'Bearer '+ bearer_token + '', 'User-Agent': 'science analysis client'}
    r = requests.get(url, headers=headers)
    #print(r.text)
    counter = 0
    tweet_dictionary = json.loads(r.text)
    testliste = [tweet_dictionary['statuses']]
    with open('datamining_{}.txt'.format(d), 'w') as f:
        for items in testliste:
            for item in items:
                f.write(item['created_at']+"\n")
                f.write(item['id_str']+"\n")
                f.write(str(item['text'].encode('UTF-8'))+"\n\n")
    f.close()
    



super_fast_hashtag_query(query)

# **************      for the DF we need      ************** #
# - time or tweetID as index
# - hashtags
# - userID
# - tweettext
