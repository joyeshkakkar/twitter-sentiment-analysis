import tweepy
import sys
import json
from textwrap import TextWrapper
from datetime import datetime
from elasticsearch import Elasticsearch
from twitterapistuff import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

es = Elasticsearch('http://elastic:changeme@localhost:9200')


class StreamListener(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            # print 'n%s %s' % (status.author.screen_name, status.created_at)

            json_data = status._json
            # print json_data['text']

            es.create(index="idx_twp",
                      doc_type="twitter_twp",
                      body=json_data
                      )
            print json_data

        except Exception, e:
            print e
            pass


streamer = tweepy.Stream(auth=auth, listener=StreamListener(), timeout=3000000000)

# Fill with your own Keywords bellow
terms = ['blackfriday', 'thanksgiving']

streamer.filter(None, terms)
# streamer.userstream(None)
