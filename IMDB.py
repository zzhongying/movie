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

d_type = [{'en': 'Adventure', 'zh': '冒险', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#CDAA7D',
           'textColor': '#8B7E66', 'waveTextColor': '#EED8AE', 'waveColor': '#CDAA7D'},
          {'en': 'Comedy', 'zh': '喜剧', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#178BCA',
           'textColor': '#045681', 'waveTextColor': '#A4DBf8', 'waveColor': '#178BCA'},
          {'en': 'Fantasy', 'zh': '幻想', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#008B00',
           'textColor': '#006400', 'waveTextColor': '#9AFF9A', 'waveColor': '#008B00'},
          {'en': 'Mystery', 'zh': '悬念', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#9ACD32',
           'textColor': '#458B00', 'waveTextColor': '#FFFFE0', 'waveColor': '#9ACD32'},
          {'en': 'Thriller', 'zh': '惊悚', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#8EE5EE',
           'textColor': '#00868B', 'waveTextColor': '#FFFAFA', 'waveColor': '#8EE5EE'},
          {'en': 'Documentary', 'zh': '记录', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#AA7D39',
           'textColor': '#8B4500', 'waveTextColor': '#D4AB6A', 'waveColor': '#AA7D39'},
          {'en': 'War', 'zh': '战争', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#696969',
           'textColor': '#000000', 'waveTextColor': '#FFFAFA', 'waveColor': '#696969'},
          {'en': 'Western', 'zh': '西部', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#DB7093',
           'textColor': '#B03060', 'waveTextColor': '#FFE4E1', 'waveColor': '#DB7093'},
          {'en': 'Romance', 'zh': '爱情', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#FF8C00',
           'textColor': '#CD661D', 'waveTextColor': '#FFDEAD', 'waveColor': '#FF8C00'},
          {'en': 'Drama', 'zh': '剧情', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#20B2AA',
           'textColor': '#668B8B', 'waveTextColor': '#B0E0E6', 'waveColor': '#20B2AA'},
          {'en': 'Horror', 'zh': '恐怖', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#000000',
           'textColor': '#000000', 'waveTextColor': '#BEBEBE', 'waveColor': '#000000'},
          {'en': 'Action', 'zh': '动作', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#CD2626',
           'textColor': '#8B1A1A', 'waveTextColor': '#FFFAFA', 'waveColor': '#CD2626'},
          {'en': 'Sci-Fi', 'zh': '科幻', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#FFD700',
           'textColor': '#8B7500', 'waveTextColor': '#FFFAFA', 'waveColor': '#FFD700'},
          {'en': 'Music', 'zh': '音乐', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#9932CC',
           'textColor': '#551A8B', 'waveTextColor': '#D8BFD8', 'waveColor': '#9932CC'},
          {'en': 'Family', 'zh': '家庭', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#CD96CD',
           'textColor': '#68228B', 'waveTextColor': '#FFFAFA', 'waveColor': '#CD96CD'},
          {'en': 'Crime', 'zh': '犯罪', 'like': 0, 'money_max': 0, 'money_min': 0, 'circleColor': '#CCCC33',
           'textColor': '#556B2F', 'waveTextColor': '#FFFAFA', 'waveColor': '#CCCC33'},
          ]
table_massage={}
enter={}

@app.route('/data/', methods=['GET'])
def data():
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

    #取各种类型中的票房最大值和最小值
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
    #print(table_massage)
    return jsonify(d_type)


@app.route('/tabs_data/',methods=['GET'])
def tabs_data():
    Level_1=xunlian.query.filter(xunlian.level).distinct().all()
    l_1=list(set(Level_1))
    print(l_1)
    return render_template('index.html')

#返回tabs页面中的内容
@app.route('/massage/')
def massage():
    #print(table_massage)
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
        return render_template('index.html')

@app.route('/ball/')
def ball():
    return render_template('ball.html')

@app.route('/gauge/')
def gauge():
     return render_template('gauge.html')

if __name__ == '__main__':
    app.run(debug=True,port=9000)