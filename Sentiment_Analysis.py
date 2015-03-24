import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

## Sample code used from https://gist.github.com/fnielsen/4183541##
# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = 'AFINN/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ 
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")

def sentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence. 
    """
    words = pattern_split.split(text.lower())
    sentiments = map(lambda word: afinn.get(word, 0), words)
    if sentiments:
        # How should you weight the individual word sentiments? 
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
        
    else:
        sentiment = 0
    return sentiment

###################################################
tweets_data_path = 'twitter_data_2.txt'
#tweets_data_path = 'twitter_data.txt'
																													
tweets_data = []
tweets_file = open(tweets_data_path, "r")

#I was getting errors (KeyError) mapping the array of tweets to
#a pandas DataFrame when using the entire set of data
#So I am using a limited set here (8952 was the max I could use
#without getting any errors)
counter = 0
number_of_tweets = 8952
for line in tweets_file:
	try:
		if counter < number_of_tweets:
			tweet = json.loads(line)
			tweets_data.append(tweet)
			counter += 1
	except:
		continue
		

total = len(tweets_data)

tweets = pd.DataFrame()
tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['retweet_count'] = map(lambda tweet: tweet['retweet_count'], tweets_data)
tweets['user'] = map(lambda tweet: tweet['user']['screen_name'], tweets_data)
tweets['name'] = map(lambda tweet: tweet['user']['name'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

#some text sanitisation
for i in range(0, total):
	#remove links using regular expression
	tweets['text'][i] = re.sub(r"http\S+", "", tweets['text'][i])
	#remove @username	
	tweets['text'][i] = re.sub( r'(^|[^@\w])@(\w{1,15})\b', "", tweets['text'][i])

#function used for filtering the tweets by keyword
def word_in_text(word,text):
	word = word.lower()
	text = text.lower()
	match = re.search(word,text)
	if match:
		return True
	return False

#Show the top 5 countries
tweets_by_country = tweets['country'].value_counts()
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize = 15)
ax.tick_params(axis='y', labelsize = 10)
ax.set_xlabel('Countries', fontsize = 15)
ax.set_ylabel('Number of Tweets', fontsize = 15)
ax.set_title('Top 5 countries', fontsize = 15, fontweight = 'bold')
tweets_by_country[:5].plot(ax=ax, kind = 'bar', color = 'blue')
plt.show()


tweets['david cameron'] = tweets['text'].apply(lambda tweet: word_in_text('david cameron', tweet))
tweets['nigel farage'] = tweets['text'].apply(lambda tweet: word_in_text('nigel farage', tweet))
tweets['ed miliband'] = tweets['text'].apply(lambda tweet: word_in_text('ed miliband', tweet))
tweets['nick clegg'] = tweets['text'].apply(lambda tweet: word_in_text('nick clegg', tweet))

total_cameron = int(tweets['david cameron'].value_counts()[True])
total_farage = int(tweets['nigel farage'].value_counts()[True])
total_miliband = int(tweets['ed miliband'].value_counts()[True])
total_clegg = int(tweets['nick clegg'].value_counts()[True])

sentiment_cameron = 0
sentiment_farage = 0
sentiment_miliband = 0
sentiment_clegg = 0

cameron_tweets = []
farage_tweets = []
miliband_tweets = []
clegg_tweets = []

#calculate average sentiment for each politician
print "---------------------------------------------"
print "Average sentiment based on the entire dataset (" + str(total) + " tweets)"
print "---------------------------------------------"

for i in range(0,total):
	if tweets['david cameron'][i]:
		text = tweets['text'][i]
		cameron_tweets.append(text)
		sentiment_cameron += sentiment(text)

sentiment_cameron /= total_cameron
print "David Cameron: " + str(sentiment_cameron) + "   (" + str(total_cameron) + " tweets)"	

for i in range(0,total):
	if tweets['nigel farage'][i]:
		text = tweets['text'][i]
		farage_tweets.append(text)
		sentiment_farage += sentiment(text)

sentiment_farage /= total_farage
print "Nigel Farage: " + str(sentiment_farage) + "   (" + str(total_farage) + " tweets)"	

for i in range(0,total):
	if tweets['ed miliband'][i]:
		text = tweets['text'][i]
		miliband_tweets.append(text)
		sentiment_miliband += sentiment(text)

sentiment_miliband /= total_miliband
print "Ed Miliband: " + str(sentiment_miliband) + "   (" + str(total_miliband) + " tweets)"	

for i in range(0,total):
	if tweets['nick clegg'][i]:
		text = tweets['text'][i]
		clegg_tweets.append(text)
		sentiment_clegg += sentiment(text)

sentiment_clegg /= total_clegg
print "Nick Clegg: " + str(sentiment_clegg) + "   (" + str(total_clegg) + " tweets)"	

average_sentiment = {'David Cameron': sentiment_cameron, 'Nigel Farage': sentiment_farage, 'Ed Miliband' : sentiment_miliband, 'Nick Clegg' : sentiment_clegg}

#####plotting results on a histogram#######
X = np.arange(len(average_sentiment))
plt.title("Average Sentiment on political party leaders")
plt.bar(X, average_sentiment.values(), align = 'center', width = 0.75)
plt.xticks(X, average_sentiment.keys())
plt.ylim(-0.5, 0.5)
plt.show()
###########################################

import random
if total > 8000:
	limit = 1000
else:
	limit = 100
#calculate average based on an equal number of randomly selected tweets
print "---------------------------------------------"
print "Average sentiment based on " + str(limit) + " randomly selected tweets"
print "---------------------------------------------"

#reset sentiment values
sentiment_cameron = 0
sentiment_farage = 0
sentiment_miliband = 0
sentiment_clegg = 0



random.shuffle(cameron_tweets)
for i in range(0,limit):
	text = cameron_tweets[i]	
	sentiment_cameron += sentiment(text)	
sentiment_cameron /= limit
print "David Cameron: " + str(sentiment_cameron) 	

random.shuffle(farage_tweets)
for i in range(0,limit):
	text = farage_tweets[i]	
	sentiment_farage += sentiment(text)
sentiment_farage /= limit
print "Nigel Farage: " + str(sentiment_farage) 		
	

random.shuffle(miliband_tweets)
for i in range(0,limit):
	text = miliband_tweets[i]	
	sentiment_miliband += sentiment(text)
sentiment_miliband /= limit
print "Ed Miliband: " + str(sentiment_miliband) 	
	

random.shuffle(clegg_tweets)
for i in range(0,limit):
	text = clegg_tweets[i]	
	sentiment_clegg += sentiment(text)
sentiment_clegg /= limit
print "Nick Clegg: " + str(sentiment_clegg) 		

			
print "---------------------------------------------"
print "Sample Output on single sentences"
print "---------------------------------------------"
#Positive statement
text = "I love my car"
print("%6.2f %s" % (sentiment(text), text))

#Negative statement
text = "I hate Mondays"
print("%6.2f %s" % (sentiment(text), text))

#Randomly selected tweet
text = cameron_tweets[random.randint(0,len(cameron_tweets))]
print("%6.2f %s" % (sentiment(text), text))

