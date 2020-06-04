# Twitter_Conversations
Scrapes Tweets and fills out conversation trees

## Authentication 
consumer_key = XXXXXX  
consumer_secret = XXXXXX  
access_key = XXXXXX  
access_secret = XXXXXX  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_key, access_secret)  
api = tweepy.API(auth)  

#### Create Tweet Object From Tweepy Search API
my_tweet = Tweet().fromTweepy('TWEET ID', api)

#### Create Tweet Lineage from leaf tweet to root tweet
my_lineage = Lineage(my_tweet, api)

#### Create and fill out Conversation
my_conversation = Conversation(my_lineage, api)

#### Create nested dictionary of conversation
d = {}  
d = writeDict(my_lineage.rootTweet, d)
