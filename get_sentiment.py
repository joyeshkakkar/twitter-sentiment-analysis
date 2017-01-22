import load_classifier as classifier

# Test the  classifier
test_tweets = list()
test_tweets.append('internship!!!')
test_tweets.append('This movie was awesome! The acting was great, plot was wonderful, and there were pythons...so yea!')
test_tweets.append('This movie was utter junk. There were absolutely 0 pythons. I don\'t see what the point was at all.'
                   ' Horrible movie, 0/10')
test_tweets.append('bad things are happening in this world!!!')

for tweet in test_tweets:
    print classifier.get_sentiment(tweet)