import re
from clean_tweet import clean_tweet
import csv
import nltk
from nltk.classify.util import apply_features
import pickle
from file_funcs import *
import datetime
__author__ = 'joyesh kakkar'

# Some Rules
# Stop words - a, is, the, with etc. The full list of stop words can be found at Stop Word List.
# These words don't indicate any sentiment and can be removed.
# Punctuation - we can remove punctuation such as comma, single/double quote, question marks at the start and end of
# each word. E.g. beautiful!!!!!! replaced with beautiful
# Words must start with an alphabet - For simplicity sake, we can remove all those words which
# don't start with an alphabet. E.g. 15th, 5.34am
# look for two or more repetitive char and replace with single ch

all_features = list()

# read stopwords from file and return it
def stop_word_list(stop_word_file):
    stop_words = list()
    stop_words.append('AT_USERNAME')
    stop_words.append('URL')

    f = open(stop_word_file, 'r')
    for line in f:
        word = line.strip()
        stop_words.append(word)
    f.close()
    return stop_words


def build_feature_vector(tweet):
    features = []
    stop_words = stop_word_list('./training_data/stopwords.txt')
    words = tweet.split()
    for w in words:
        # replace two or more char with two occurrences
        # w=replace_rep_char(w)
        # strip punctuation
        w = w.strip('\'"?.,')
        # check if word start with alphabet
        val = re.search(r'^[a-zA-Z][a-zA-Z0-9]*$', w)
        # ignore if it's stop word
        if w in stop_words or val is None:
            continue
        else:
            features.append(w.lower())
    return features


def get_feature_list(feature_list_file_name):
    feature_list = list()
    f = open(feature_list_file_name, 'r')
    for line in f:
        feature_list.append(line.strip())
    f.close()
    return feature_list


# Storing the feature vector in a list that can be used to train the classifier
feature_list = get_feature_list('./training_data/full_feature_list.txt')
# Remove featureList duplicate
unique_feature_list = list(set(feature_list))


# Extracting words in a proper format that are relevant to tweets
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in unique_feature_list:
        features['contains(%s)' % word] = (word in tweet_words)
    return features


def main():
    start_time = datetime.datetime.now().replace(microsecond=0)
    remove_file_if_exists('./training_data/full_feature_list.txt')
    # Below is the list of tuples tweet features, sentiment
    tweets = []
    input_tweets = csv.reader(open('./training_data/training_dataset.csv', 'rb'), delimiter=',')

    # Open the below file for writing
    f = open('./training_data/full_feature_list.txt', 'w')
    for row in input_tweets:
        sentiment = row[0]
        tweet = row[1]
        # Calling process_tweet method to pre process the tweet
        processed_tweet = clean_tweet(tweet)
        # Calling build_feature_list that returns the list of feature vector
        tweet_features = build_feature_vector(processed_tweet)
        for feature in tweet_features:
            f.write(feature)
            f.write('\n')
        all_features.append(tweet_features)
        tweets.append((tweet_features, sentiment))
    f.close()
    print 'input tweets are cleaned, features are extracted.'
    # In below function the inputs are extract features function and all
    # tweets, the extract features function picks one tweet from list if tweets and create feature vector.
    print 'Generating training set.'
    training_set = apply_features(extract_features, tweets)
    print 'training set generated.'

    print 'training naive bayes classifier'
    nb_classifier = nltk.NaiveBayesClassifier.train(training_set)
    f = open('./output/NBClassifier_trained_21k_tweets.pickle', 'wb')
    pickle.dump(nb_classifier, f)
    f.close()
    print 'classifier trained and pickled.'

    # Print most informative features about the classifier
    print nb_classifier.show_most_informative_features(10)

    end_time = datetime.datetime.now().replace(microsecond=0)
    print "Total time taken-->", end_time-start_time

if __name__ == '__main__':
    main()
