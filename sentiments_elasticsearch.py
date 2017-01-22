import load_classifier as classifier
import json
import pandas
from elasticsearch import Elasticsearch
from pyelasticsearch import ElasticSearch
from es_indexer import es_indexer
from datetime import datetime


def get_tweets():
    tweets_lst = []
    f = open('./output/tweet_collection.txt')
    tweets_data = []
    for line in f:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    print" Analyzing %d tweets" % len(tweets_data)

    # Use pandas to simplify data manipulation:
    # Creating a data frame : Its a row-column data structure
    tweets = pandas.DataFrame()

    tweets["text"] = map(lambda tweet: tweet["text"], tweets_data)
    for i in range(len(tweets)):
        tweets_lst.append(tweets['text'][i])
    f.close()
    return tweets_lst


def main():
    es = Elasticsearch('http://elastic:changeme@localhost:9200')
    ###########Indexing into Elasticsearch############
    id = 0
    tweets = get_tweets()
    for tweet in tweets:
        id += 1
        sentiment = classifier.get_sentiment(tweet)
        es.index(index="sentiment_analysis", body={
            "text": tweet,
            "sentiment": sentiment
        }, id=id, doc_type="tweet")
        print "Indexed %d tweets." % id
    print "Indexing completed."
    es.indices.refresh(index="sentiment_analysis")
    print "Index refreshed."


if __name__ == '__main__':
    main()
