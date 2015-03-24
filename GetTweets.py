#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "2844386922-Qotx3tu61PM6qeIC7lE6I3G8oCoqiGUJEv2ZwVe"
access_token_secret = "lUToCkc1DI5geh0ZfWTySrlbIC8hfrQCDRGjKQqU9tOJH"
consumer_key = "hqNJ7kcXo00K4sRm31VqwKWR4"
consumer_secret = "cqeF4r3nn8JXI4HjIwFuEB3v6yw31WZiDkOdTMzyRgcMMos4PU"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 
    stream.filter(track=['david cameron', 'ed miliband', 'nick clegg', 'nigel farage'])
