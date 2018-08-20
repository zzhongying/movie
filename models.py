from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


class xunlian(db.Model):
    __tablename__='xl'
    name= db.Column(db.String(255), primary_key=True)
    years= db.Column(db.String(255))
    director= db.Column(db.String(255))
    country= db.Column(db.String(255))
    language= db.Column(db.String(255))
    invest= db.Column(db.String(255))
    type= db.Column(db.String(255))
    key_words= db.Column(db.String(255))
    screen= db.Column(db.String(255))
    face= db.Column(db.String(255))
    dir_like= db.Column(db.String(255))
    time = db.Column(db.String(255))
    color= db.Column(db.String(255))
    level= db.Column(db.String(255))
    act_one= db.Column(db.String(255))
    act_one_like=db.Column(db.String(255))
    act_two= db.Column(db.String(255))
    act_two_like= db.Column(db.String(255))
    act_three= db.Column(db.String(255))
    act_three_like= db.Column(db.String(255))
    act_all_like= db.Column(db.String(255))
    like_all= db.Column(db.String(255))
    pro_review=db.Column(db.String(255))
    user_review=db.Column(db.String(255))
    film_fb_like=db.Column(db.String(255))
    IMDB=db.Column(db.String(255))
    Box_office=db.Column(db.String(255))
    link=db.Column(db.String(255))