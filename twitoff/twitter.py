from numpy import vectorize
import tweepy
from os import getenv
import spacy
from .models import db, User, Tweet

# create authentication and connect twitter
TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')
auth = tweepy.OAuthHandler(
    TWITTER_API_KEY,
    TWITTER_API_KEY_SECRET
)
twitter = tweepy.API(auth)

# load the word2vec model from folders and utilize it in
# creating a function that vectorizes the tweets
w2v_model = spacy.load("my_word2vec_model")

def vectorize_tweet(tweet_text):
    return w2v_model(tweet_text).vector


def add_or_update_user(user_name):

    try: 
        # find the user by user_name
        twitter_user = twitter.get_user(
            screen_name= user_name
        )
        # update or add the new user to the db
        user = User.query.get(twitter_user.id) or User(
            id=twitter_user.id, name=user_name)
        db.session.add(user)

        # retrieve the most recent tweets from this user
        user_tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="Extended",
            since_id=user.newest_tweet_id
        )

        # if there a new tweet, save the newest tweet id
        if user_tweets:
            user.newest_tweet_id = user_tweets[0].id

        for tweet in user_tweets:
            # vectorize each tweet
            tweet_vec = vectorize_tweet(tweet.text)
            # adding the tweet into the Tweet table
            db_tweet = Tweet(
                id = tweet.id,
                tweet = tweet.text,
                tweet_vect = tweet_vec
            )
            # adding each Tweet object to the backref tweets
            user.tweets.append(db_tweet)
            db.session.add(db_tweet)
        
    except Exception as e:
        print('Error processing {}: {}'.format(user_name, e))
        raise e

    else:
        db.session.commit()