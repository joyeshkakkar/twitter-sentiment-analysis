from twitterapistuff import *
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from file_funcs import *
import load_classifier as classifier
import json
import pandas
from elasticsearch import Elasticsearch
import pprint
__author__ = 'joyeshkakkar'


# This is a listener for hearing data
class TwitterStreamListener(StreamListener):
    def on_data(self, data):
        global index_count, index_name
        index_count += 1
        # print data
        # print type(data)
        data = json.loads(data)
        # print type(data)
        # pprint.pprint (data.keys())
        if 'text' in data.keys():
            tweet = data["text"]
            print tweet
            sentiment = classifier.get_sentiment(tweet)
            print sentiment
            print "Processed %d tweets." % index_count
            es.index(index= index_name, body={
                "text": tweet,
                "sentiment": sentiment
            }, id=index_count, doc_type="tweet")
            es.indices.refresh(index="sent_stream")
        return True

    def on_error(self, status_code):
        print 'Encountered Error with Status Code:', status_code

    def on_timeout(self):
        print "Timeout....."
        return True

    def get_tweets(self):
        # Enter consumer_key, consumer_secret to create a OAuth handler
        auth = OAuthHandler(consumer_key, consumer_secret)
        # access_token, access_token_secret
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, listener, timeout=120)
        stream.filter(track=topic)


es = Elasticsearch('http://elastic:changeme@localhost:9200')
index_name = 'sent_stream'
try:
    es.indices.delete(index=index_name, ignore=[400, 404])
    # es.indices.delete(index='sentiment_analysis', ignore=[400, 404])
    print "Deleted index %s as it already existed." % index_name
except:
    print "Index %s did not exist." % index_name
index_count = 0
# remove_file_if_exists('./output/tweet_collection.txt')
topic = ['lewis hamilton']
listener = TwitterStreamListener()
listener.get_tweets()

