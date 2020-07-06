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

#### Create Tweet Object using the Tweet ID
my_tweet = Tweet().tweet_by_id('TWEET_ID', api)

#### Create Tweet Lineage from leaf tweet to root tweet
my_lineage = Lineage(my_tweet, api)

#### Create and fill out Conversation
my_conversation = Conversation(my_lineage, api)

#### Create nested dictionary of conversation
d = {}  
d = writeDict(tweetDict=d, conv=my_conversation)

#### Option to use backup query method that returns a tweet
my_tweet = Tweet().tweet_by_id('TWEET_ID', api, backup_query)
my_lineage = Lineage(my_tweet, api, backup_query)
my_conversation = Conversation(my_lineage, api, backup_query)

#### Limitations
- fillTree function of Conversation class cannot grab tweets stemming from deleted quote tweets
- fillTree function of Conversation class cannot detect deleted tweets when traversing down a conversation
- deleted tweets are only detected when traversing up a lineage, using the traverse function in the Lineage class

