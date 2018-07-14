from flask import Flask,render_template,request, jsonify,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_cors import *
from sqlalchemy.ext.declarative import declarative_base
import config
from sqlalchemy import distinct
from models import xunlian
import contextlib

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

@app.route('/data/',methods=['GET'])
def data():
    ALL=xunlian.query.filter(xunlian.country=='USA').all()
    all_data={}
    ALLDATA=[]
    while len(ALL)>0:
        all_xl=ALL.pop()
        all_data['NAME']=all_xl.name
        ALLDATA.append(all_data)
        print(ALLDATA)
        all_data={}

    return jsonify(ALLDATA)

@app.route('/ball_data/')
def ball_data():
    ALL = xunlian.query.all()
    Money=[]
    money_max=[]
    while len(ALL) > 0:
        Ball=ALL.pop()
        money=Ball.Box_office
        if money=='':
            money=0
        money=int(money)
        Money.append(money)
    money_max.append(max(Money))
    print(money_max)

    return jsonify(money_max)


@app.route('/tabs_data/',methods=['GET'])
def tabs_data():
    Level_1=xunlian.query.filter(xunlian.level).distinct().all()
    l_1=list(set(Level_1))
    print(l_1)
    return render_template('index.html')

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/tabs/',methods=['GET','POST'])
def tabs():
    if request.method=='GET':
        return render_template('tabs.html')
    else:
        name= request.form.get('name')
        director=request.form.get('director')
        act_1=request.form.get('act_1')
        act_2=request.form.get('act_2')
        act_3 = request.form.get('act_3')
        type=request.form.get('type')
        invest=request.form.get('invest')
        key_words=request.form.get('key_words')

        return render_template('index.html')

@app.route('/ball/')
def ball():

    return render_template('ball.html')

@app.route('/gauge/')
def gauge():

     return render_template('gauge.html')

if __name__ == '__main__':
    app.run(debug=True)