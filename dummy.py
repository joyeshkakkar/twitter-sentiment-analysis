import pandas
import json
import pprint
def tweet_data():
    tweets_lst = []
    fhand = open('./output/tweet_collection.txt')
    tweets_data = []
    for line in fhand:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
            break
        except:
            continue
    # print" Analyzing %d tweets" % len(tweets_data)
    fhand.close()
    # Use pandas to simplify data manipulation:
    # Creating a data frame : Its a row-column data structure
    # print tweets['text'][0]
    return tweets_data[0]['text']

pprint.pprint(tweet_data())
