from twitterapistuff import *
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from file_funcs import *
import load_classifier as classifier
import json

__author__ = 'joyeshkakkar'


# This is a listener for hearing data
class TwitterStreamListener(StreamListener):
    def on_data(self, data):
        print data
        # try:
        #     data = json.loads(data)
        #     if 'text' in data.keys():
        #         tweet = data["text"]
        #         print "tweet-->", tweet
        #         sentiment = classifier.get_sentiment(tweet)
        #         print "sentiment, tweet-->", sentiment, tweet
        # except:
        #     print "Exception occured"
        f = open('./output/tweet_collection.txt', 'a')
        f.write(data)
        f.close()
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

count = 0
remove_file_if_exists('./output/tweet_collection.txt')
topic = ['thanksgiving']
listener = TwitterStreamListener()
listener.get_tweets()

