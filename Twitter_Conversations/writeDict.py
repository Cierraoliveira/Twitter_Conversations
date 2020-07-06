from Twitter_Conversations.Tweet import Tweet
from Twitter_Conversations.Conversation import Conversation


# Function to create dictionary for JSON string
def writeDict(tweetDict: dict, tweet: Tweet=None, conv: Conversation=None):
    # dictionary for highest tweet in conversation
    if conv:
        tweet = conv.tree[0]
        tweetDict = dict(id=tweet.tweet_id, text=tweet.tweet_text, children=[],
                         type=tweet.tweet_type, replyID=tweet.reply_id, num_retweets=tweet.retweets)

    if tweet.children:
        for i in tweet.children:
            sub_dict = dict(id=i.tweet_id, text=i.tweet_text, children=[], type=i.tweet_type,
                            replyID=i.reply_id, num_retweets=i.retweets)
            # recursively call function
            writeDict(tweetDict=sub_dict, tweet=i)
            # add broken head to empty dictionary
            if i.tweet_type == 'broken_head':
                y = dict(id=None, text=None, children=[], type=None, replyID=None, num_retweets=None)
                y['children'].append(sub_dict)
                tweetDict['children'].append(y)
            else:
                tweetDict['children'].append(sub_dict)

    return tweetDict
