# twitter-sentiment-analysis
Twitter sentiment analyzer<br/><br/>

T<b>echnologies:</b><br/>
NLTK, Elastisearch and Kibana.<br/><br/>

<b>Description:</b><br/>
1. A Naive Bayes Classifier is trained on a set of 21k tweets. It is then used to classify live Twitter streams as positive, negative and netural.<br/>
2. Tweepy (Twitter API) was used to stream live tweets for a topic (input to program). <br/>
3. Sentiments which were output of the classifier were indexed using Elasticsearch. <br/>
4. Kibana was used for plotting graphs of sentiments predicted by live tweets. <br/><br/>

<b>Steps:<b/><br/>
1. Clone the repository.<br/>
2. Run the files in following order<br/>
    a. train_classifier.py<br/>
    b. load_classifier.py<br/>
    c. twitter_stream.py<br/>
