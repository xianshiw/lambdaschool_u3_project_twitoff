from flask import Flask
from flask import render_template
from flask import request
from .models import db, User, Tweet
from os import getenv
from .twitter import add_or_update_user
from .predict import predict

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # create tables
    with app.app_context():
        db.create_all()

    @app.route('/')
    def root():
        return render_template("home.html", title="Home", users = User.query.all())

    @app.route('/reset')
    def refresh_db():
        db.drop_all()
        db.create_all()
        return render_template("home.html", title="Reset Database")

    @app.route('/user', methods=["POST"])
    @app.route('/user/<name>', methods=["GET"])
    def user(name=None, message=''):

        # Pull name from the user input in webpage
        name = name or request.values['name']
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = "User {} successfully added".format(name)

            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)

    @app.route('/predict', methods=["POST"])
    def predict_user():

        user0 = request.values['user0']
        user1 = request.values['user1']
        rand_tweet = request.values['tweet_text']

        if user0 == user1:
            message = "Cannot compare the same user"
        else:
            prediction = predict(
                user0,
                user1,
                rand_tweet
            )
            if prediction == 0:
                morelikely = user0
                lesslikely = user1
            else:
                morelikely = user1
                lesslikely = user0
            message = "'{}' is more likely to be sent by {} than {}.".format(
                rand_tweet,
                morelikely,
                lesslikely
            )
        return render_template('predict.html', title="Prediction", message=message)

    @app.route('/update')
    def update():

        usernames = User.query.all()
        for user in usernames:
            add_or_update_user(user)
        return render_template("home.html", title="Home", users = User.query.all())
        
    return app