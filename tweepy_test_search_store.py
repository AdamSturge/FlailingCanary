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
	# BEGIN GETTING TWEETS
	auth = OAuthHandler(config.consumer_key, config.consumer_secret)
	auth.set_access_token(config.access_token, config.access_token_secret)
	api_inst = API(auth, parser = parsers.JSONParser())
	l = api_inst.search(q="haircut", count=3)
	# END GETTING TWEETS
	
	#BEGIN CONENCTING TO DATABASE
	connection = pymysql.connect(host = config.host, user = config.user, password = config.password, db = config.database, cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()
	# END CONENCTING TO DATABASE
	
	#BEGIN DEFINING QUERY
	sql = "INSERT INTO tweets (tweet_text,hashtags,lang,urls,trending,user_id,retweet_count,source,possibly_sensative) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	#END DEFINING QUERY
	
	# BEGIN EXTRACTING TWEET INFO
	for tweet in l["statuses"] :
		tweet_text    = tweet["text"].encode('utf-8') if ("text" in tweet) else ""
		lang          = tweet["lang"].encode('utf-8') if ("lang" in tweet) else ""
		source        = tweet["source"].encode('utf-8') if ("source" in tweet) else ""
		sensitive     = tweet["possibly_sensitive"] if ("possibly_sensitive" in tweet) else False
		retweet_count = tweet["retweet_count"] if ("retweet_count" in tweet) else 0
		trending      = tweet["trending"].encode('utf-8') if ("trending" in tweet) else "" # GOING TO HAVE TO REMOVE THIS, IT DOESN'T SHOW UP IN SEARCH (DOES IN STREAM THOUGH)
		
		if "entities" in tweet :
			hashtags = tweet["entities"]["hashtags"] if ("hashtags" in tweet["entities"]) else [""]
			urls     = tweet["entities"]["urls"] if ("urls" in tweet["entities"]) else [""]
		else :
			hashtags = [""]
			urls = [""]
		
		if "user" in tweet :
			user_id = tweet["user"]["id"] if "id" in tweet["user"] else -1
		else :
			user_id = -1
			
		#BEGIN INSERTING DATA INTO DATABASE
		hashtags = ",".join(hashtags).encode('utf-8')
		urls     = ",".join(urls).encode('utf-8')
		
		cursor.execute(sql,(tweet_text,hashtags,lang,urls,trending,user_id,retweet_count,source,sensitive))
		connection.commit()
		print("Got one")
		#END INSERTING DATA INTO DATABASE
	# END EXTRACTING TWEET INFO
