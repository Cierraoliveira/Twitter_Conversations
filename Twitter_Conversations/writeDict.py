from Twitter_Conversations.Tweet import Tweet


# Function to create dictionary for JSON string
def writeDict(tweet: Tweet, tweetDict: dict):
    # dictionary for root tweet
    if tweet.tweet_type == 'root':
        tweetDict = dict(id=tweet.tweet_id, text=tweet.tweet_text, children=[],
                         type=tweet.tweet_type, replyID=tweet.reply_id, num_retweets=tweet.retweets)

    if tweet.children:
        for i in tweet.children:
            x = dict(id=i.tweet_id, text=i.tweet_text, children=[], type=i.tweet_type,
                     replyID=i.reply_id, num_retweets=i.retweets)

            # recursively call function
            writeDict(i, x)

            # add broken head to empty dictionary
            if i.tweet_type == 'broken_head':
                y = dict(id=None, text=None, children=[], type=None, replyID=None, num_retweets=None)
                y['children'].append(x)
                tweetDict['children'].append(y)
            else:
                tweetDict['children'].append(x)

    return tweetDict
