import base64
import ignore
import json
import requests
import datetime
import time

consumer_key = ignore.TWITTER_CONSUMER_KEY
consumer_secret = ignore.TWITTER_CONSUMER_SECRET
access_token = ignore.TWITTER_ACCESS_TOKEN
access_secret = ignore.TWITTER_ACCESS_SECRET

#in order to only get minutious file names we set the second and microsecond
#in the datetime to 0
d = str(datetime.datetime.now().replace(second=0, microsecond=0))


#this specifies the date 7 days back in order to retrieve tweets that were posted within the last 7 days
today = datetime.date.today() + datetime.timedelta(days=1)
lastweek = today - datetime.timedelta(days=3)


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
query ='%23ICURehab'
zaehler = 0
#still needs to be implemented
def replace_non_ascii(query):
    print(query)


def super_fast_hashtag_query(query, lastid = 0):
    bearer_token = ignore.BEARER_TOKEN

    if lastid == 0:
        url = 'https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=recent&since={}&until={}&count=10000'.format(query, lastweek, today)
        schreibtyp = 'w'


    else:
        url = 'https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=recent&max_id={}&count=10000'.format(query, lastid)
        schreibtyp = 'a'


    headers = {'Authorization': 'Bearer '+ bearer_token + '', 'User-Agent': 'science analysis client'}
    r = requests.get(url, headers=headers)
    #print(r.text)

    tweet_dictionary = json.loads(r.text)
    testliste = [tweet_dictionary['statuses']]
    data_dictionary = {}
    #letzteid = str(tweet_dictionary['search_metadata']['max_id'])
    #print (letzteid)

    # das funktioniert nicht und ich sehe den fehler nicht...
    # theoretisch soll der die letzte ID nehmen und checken ob die schon im dict
    # ist und wenn ja einfach abbrechen - aber irgendwie läuft der trotz gleich
    # bleibender ID einfach weiter... 
    for items in testliste:
        for item in items:
            #print (type(item['id_str']))

            if item['id_str'] in data_dictionary.keys():
                print("done")
                return data_dictionary

            else:
                print(item['id_str'])
                ts = time.strftime('%Y-%m-%d %H:%M', time.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                #data_dictionary[item["id_str"]] = [ts, item['user']['id_str'], item['user']['screen_name'], item['retweet_count'], str(item['text'].encode('UTF-8'))[2:-1]]
                data_dictionary[item["id_str"]] = [ts, item['user']['id_str'], item['user']['screen_name'], item['retweet_count'], str(item['text'].encode('UTF-8'))[2:-1]]
                letzteid = item['id_str']
        #if not letzteid in data_dictionary.keys():
    super_fast_hashtag_query(query, letzteid)


#this is the earliest ID of the query -> the starting point for the next query
        #




'''
    with open('files/datamining_{}.txt'.format(d), '{}'.format(schreibtyp)) as f:
            for items in testliste:
                for item in items:
                        letzteid = items[-1]['id_str']
                    #this
                    #if not 'RT' in item['text']:
                        print ("itemid: {}".format(item['id_str']))

                        global zaehler
                        f.write(str(zaehler)+"\n")
                        print(zaehler)
                        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                        f.write("{}".format(ts)+"\n")
                        f.write(item['id_str']+"\n")
                        f.write(item['user']['id_str']+"\n")
                        f.write("@"+item['user']['screen_name']+"\n")
                        f.write("retweetcount: "+str(item['retweet_count'])+"\n")
                        #f.write("favcount: "+str(item['favorite_count'])+"\n")
                        f.write(str(item['text'].encode('UTF-8'))[2:-1]+"\n\n")
                        zaehler += 1
                        if str(lastid) == str(letzteid):
                            return

'''



dic = super_fast_hashtag_query(query)
for key, value in dic.items():
    print (key, value)

# **************      for the DF we need      ************** #
# - time or tweetID as index
# - hashtags
# - userID
# - tweettext
