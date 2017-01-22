import pickle
from clean_tweet import clean_tweet
from train_classifier import extract_features, build_feature_vector

f = open('./output/NBClassifier_trained_21k_tweets.pickle')
nb_classifier = pickle.load(f)
f.close()


def get_sentiment(tweet_text):
    tweet_features = extract_features(build_feature_vector(clean_tweet(tweet_text)))
    return nb_classifier.classify(tweet_features)

