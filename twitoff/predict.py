import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict(user0_name, user1_name, rand_tweet):


    # get the two users from our database
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    # get tweet vectors for each valid tweet
    user0_vec = np.array([tweet.tweet_vect for tweet in user0.tweets])
    user1_vec = np.array([tweet.tweet_vect for tweet in user1.tweets])

    # vertically stack the two user tweets
    # (to form an X matrix)
    vects = np.vstack([user0_vec, user1_vec])
    # create a y column, label the two users as
    # 0 and 1 accordingly
    labels = np.concatenate(
        [
            np.zeros(len(user0.tweets)),
            np.ones(len(user1.tweets))
        ]
    )

    # fit the model using logistic regression
    lr_model = LogisticRegression().fit(vects, labels)

    # vectorize the client input random tweet
    rand_tweet_vec = vectorize_tweet(rand_tweet).reshape(1,-1)
    # predict which user should this random tweet belong to
    result = lr_model.predict(rand_tweet_vec)

    return result