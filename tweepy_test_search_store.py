from __future__ import absolute_import, print_function
from tweepy import OAuthHandler
from tweepy import API
from tweepy import parsers
import CanaryConfig as config
import pymysql



# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
t=[]
def storeKeyVals(data,arg_list):
    global t
    print("once")
    if isinstance(data, list):
        for item in data:
            storeKeyVals(item, arg_list)
    elif isinstance(data, dict):
        for k, v in data.items():
            if k in arg_list and not isinstance(v,dict):
                t.append([k,v])
            storeKeyVals(v, arg_list)
    else:
        pass

if __name__ == '__main__':
    connection = pymysql.connect(host = config.host, user = config.user, password = config.password, db = config.database, cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api_inst = API(auth, parser = parsers.JSONParser())
    l = api_inst.search(q="haircut", count=1)
    storeKeyVals(l,["text"])
    sql = 'INSERT INTO tweet_storage (text) VALUES ("'+str(t[0][1])+'")'
    print(sql.encode("utf-8"))
    cursor.execute(sql.encode("utf-8"))
    connection.commit()
    print("Got one")
    t = []  
