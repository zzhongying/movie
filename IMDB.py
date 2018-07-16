from flask import Flask,render_template,request, jsonify,redirect,url_for
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



@app.route('/data/', methods=['GET'])
def data():
    d_type = [{'en': 'Adventure', 'zh': '冒险', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Comedy', 'zh': '喜剧', 'like': 0, 'money_max': 0,'money_min':0},
              {'en': 'Fantasy', 'zh': '幻想', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Mystery', 'zh': '悬念', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Thriller', 'zh': '惊悚', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Documentary', 'zh': '记录', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'War', 'zh': '战争', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Western', 'zh': '西部', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Romance', 'zh': '爱情', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Drama', 'zh': '剧情', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Horror', 'zh': '恐怖', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Action', 'zh': '动作', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Sci-Fi', 'zh': '科幻', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Music', 'zh': '音乐', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Family', 'zh': '家庭', 'like': 0,'money_max':0,'money_min':0},
              {'en': 'Crime', 'zh': '犯罪', 'like': 0,'money_max':0,'money_min':0},
              ]
    # com = adv = fan = mys = thr = doc = war = wes = rom = dra = hor = act = sci = mus = fam = cri = 0
    # mytype = []
    ALL = xunlian.query.all()
    money_adv= []
    money_com=[]
    money_fan=[]
    money_mys=[]
    money_thr=[]
    money_doc=[]
    money_war=[]
    money_wes=[]
    money_rom=[]
    money_dra=[]
    money_hor=[]
    money_act=[]
    money_sci=[]
    money_mus=[]
    money_fam=[]
    money_cri=[]

    while len(ALL) > 0:
        dataset = ALL.pop()
        types = dataset.type.split("|")    #字段拆分
        like = dataset.like_all
        money=dataset.Box_office
        if like == '':
            like = 0

        if money=='':
            money=0
        # print(like)
        like = int(like)
        money=int(money)
        # print(type(like))
        # print(repr(like))
        #print(money)
        while len(types):
            count = types.pop()
            if count == d_type[0]["en"]:
                d_type[0]["like"] += like
                money_adv.append(money)
                #print(max(money_adv))
            elif count == d_type[1]["en"]:
                d_type[1]["like"] += like
                money_com.append(money)
            elif count == d_type[2]["en"]:
                d_type[2]["like"] += like
                money_fan.append(money)
            elif count == d_type[3]["en"]:
                d_type[3]["like"] += like
                money_mys.append(money)
            elif count == d_type[4]["en"]:
                d_type[4]["like"] += like
                money_thr.append(money)
            elif count == d_type[5]["en"]:
                d_type[5]["like"] += like
                money_doc.append(money)
            elif count == d_type[6]["en"]:
                d_type[6]["like"] += like
                money_war.append(money)
            elif count == d_type[7]["en"]:
                d_type[7]["like"] += like
                money_wes.append(money)
            elif count == d_type[8]["en"]:
                d_type[8]["like"] += like
                money_rom.append(money)
            elif count == d_type[9]["en"]:
                d_type[9]["like"] += like
                money_dra.append(money)
            elif count == d_type[10]["en"]:
                d_type[10]["like"] += like
                money_hor.append(money)
            elif count == d_type[11]["en"]:
                d_type[11]["like"] += like
                money_act.append(money)
            elif count == d_type[12]["en"]:
                d_type[12]["like"] += like
                money_sci.append(money)
            elif count == d_type[13]["en"]:
                d_type[13]["like"] += like
                money_mus.append(money)
            elif count == d_type[14]["en"]:
                d_type[14]["like"] += like
                money_fam.append(money)
            elif count == d_type[15]["en"]:
                d_type[15]["like"] += like
                money_cri.append(money)

    d_type[0]['money_max']=max(money_adv)
    d_type[1]['money_max'] = max(money_com)
    d_type[2]['money_max'] = max(money_fan)
    d_type[3]['money_max'] = max(money_mys)
    d_type[4]['money_max'] = max(money_thr)
    d_type[5]['money_max'] = max(money_doc)
    d_type[6]['money_max'] = max(money_war)
    d_type[7]['money_max'] = max(money_wes)
    d_type[8]['money_max'] = max(money_rom)
    d_type[9]['money_max'] = max(money_dra)
    d_type[10]['money_max'] = max(money_hor)
    d_type[11]['money_max'] = max(money_act)
    d_type[12]['money_max'] = max(money_sci)
    d_type[13]['money_max'] = max(money_mus)
    d_type[14]['money_max'] = max(money_fam)
    d_type[15]['money_max'] = max(money_cri)

    d_type[0]['money_min'] = min(money_adv)
    d_type[1]['money_min'] = min(money_com)
    d_type[2]['money_min'] = min(money_fan)
    d_type[3]['money_min'] = min(money_mys)
    d_type[4]['money_min'] = min(money_thr)
    d_type[5]['money_min'] = min(money_doc)
    d_type[6]['money_min'] = min(money_war)
    d_type[7]['money_min'] = min(money_wes)
    d_type[8]['money_min'] = min(money_rom)
    d_type[9]['money_min'] = min(money_dra)
    d_type[10]['money_min'] = min(money_hor)
    d_type[11]['money_min'] = min(money_act)
    d_type[12]['money_min'] = min(money_sci)
    d_type[13]['money_min'] = min(money_mus)
    d_type[14]['money_min'] = min(money_fam)
    d_type[15]['money_min'] = min(money_cri)

    return jsonify(d_type)


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

    return jsonify(money_max)


@app.route('/tabs_data/',methods=['GET'])
def tabs_data():
    Level_1=xunlian.query.filter(xunlian.level).distinct().all()
    l_1=list(set(Level_1))
    print(l_1)
    return render_template('index.html')

table_massage={}

@app.route('/massage/')
def massage():
    return jsonify(table_massage)

@app.route('/', methods=['GET', 'POST'])
def tabs():
    if request.method == 'GET':
        return render_template('tabs.html')
    else:
        table_massage['name'] = request.form.get('name')
        table_massage['director'] = request.form.get('director')
        table_massage['act'] = request.form.get('act').split("/")
        table_massage['type'] = request.form.get('type').split()
        table_massage['invest'] = request.form.get('invest')
        table_massage['key_word'] = request.form.get('key_words').split()
        table_massage['CBW'] = request.form.get('CBW')
        table_massage['level'] = request.form.get('level')
        dir = xunlian.query.filter(xunlian.director == table_massage['director']).all()
        dir_like = act1_like = act2_like = act3_like = 0
        act1 = xunlian.query.filter(xunlian.act_one == table_massage['act'][0]).all()
        act2 = xunlian.query.filter(xunlian.act_two == table_massage['act'][1]).all()
        act3 = xunlian.query.filter(xunlian.act_three == table_massage['act'][2]).all()
        if dir:
            i = 0
            while i < len(dir):
                dir_like = int(dir[i].dir_like)
                i += 1
            table_massage['dir_like'] = dir_like / len(dir)
        if act1:
            i = 0
            while i < len(act1):
                act1_like += int(act1[i].act_one_like)
                i = i + 1
            table_massage['act1_like'] = act1_like / len(act1)
        if act2:
            i = 0
            while i < len(act2):
                act2_like += int(act2[i].act_one_like)
                i = i + 1
            table_massage['act2_like'] = act2_like / len(act2)
        if act3:
            i = 0
            while i < len(act3):
                act3_like += int(act3[i].act_one_like)
                i = i + 1
            table_massage['act3_like'] = act3_like / len(act3)
        return redirect(url_for('index'))


@app.route('/ball/')
def ball():
    return render_template('ball.html')

@app.route('/gauge/')
def gauge():

     return render_template('gauge.html')

if __name__ == '__main__':
    app.run(debug=True)