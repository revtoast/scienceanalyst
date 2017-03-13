import base64
import ignore
import requests

consumer_key = ignore.TWITTER_CONSUMER_KEY
consumer_secret = ignore.TWITTER_CONSUMER_SECRET
access_token = ignore.TWITTER_ACCESS_TOKEN
access_secret = ignore.TWITTER_ACCESS_SECRET

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
query ='%23wurstbrotkonfetti'

def super_fast_hashtag_query(query):
    bearer_token = ignore.BEARER_TOKEN
    url = 'https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query)
    headers = {'Authorization': 'Bearer '+ bearer_token + '', 'User-Agent': 'science analysis client'}
    r = requests.get(url, headers=headers)
    hashcounter = 0
    for item in r:
        print(item)
        hashcounter += 1
    print (hashcounter)

super_fast_hashtag_query(query)
