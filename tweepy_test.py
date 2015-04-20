from __future__ import absolute_import, print_function
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json

keylist = open("config.txt").read().splitlines()


# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key    =keylist[0]
consumer_secret =keylist[1]

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token        =keylist[2]
access_token_secret =keylist[3]



def printKeyVals(data, indent=0):
    if isinstance(data, list):
        print()
        for item in data:
            print("    "*indent,end="")
            printKeyVals(item, indent+1)
    elif isinstance(data, dict):
        print()
        for k, v in data.items():
            if isinstance(v, dict):
                print("    " * indent, k + ":")
            else :
                print("    " * indent, k + ":",end ="")
            printKeyVals(v, indent + 1)
    else:
        try:
            print(data)         
        except:
            try:
                print(data.encode('utf-8'))
            except:
                print("failed to decode")


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    
    def on_data(self, data):
        tweet = json.loads(data)
        print("------------------------START TWEET--------------------------------------")
        printKeyVals(tweet)
        print("--------------------------END TWEET--------------------------------")
        return True

    def on_error(self, status):
        print("error : " + str(status))
        if (status == 420):
            #returning False in on_data disconnects the stream
            return False
        return True

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['@ClintonNews','@HillaryClinton'])

