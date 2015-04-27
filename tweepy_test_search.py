from __future__ import absolute_import, print_function
from tweepy import OAuthHandler
from tweepy import API
from tweepy import parsers
import CanaryConfig as config

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section

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

if __name__ == '__main__':
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api_inst = API(auth, parser = parsers.JSONParser())
    l = api_inst.search(q="Hillary Clinton OR Barack Obama", count=1)
    printKeyVals(l)
