from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Creates a 'user' table
class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    newest_tweet_id = db.Column(db.BigInteger
    )
    def __repr__(self):
        return "<User: {}>".format(self.name)

#Creates a 'tweet' table
class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey(
        'user.id'), nullable=False)
    tweet = db.Column(db.Unicode(300))
    user = db.relationship('User', backref=db.backref(
        'tweets', lazy=True))
    tweet_vect = db.Column(db.PickleType, nullable=False)

    def __repr__(self):
        return "<Tweet: {}>".format(self.tweet)

CREATE_USER_TABLE_SQL = """
  CREATE TABLE IF NOT EXIST user (
    id INT PRIMARY,
    name STRING NOT NULL
  );
"""