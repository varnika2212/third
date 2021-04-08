from datetime import datetime,timedelta
import time
from datetime import timezone
from flask import Flask,request, render_template
from helper import validate
from flask import jsonify
import json
import string

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False

def remove_alphabets(s):
    return ''.join(i for i in s if i.isdigit())

@app.route('/')
def index():
    return render_template('index_three.html')


@app.route('/result_three',methods=['POST'])
def result():
    if request.method=='POST':
        start_time=request.form.get('st')
        end_time=request.form.get('et')
        counter=0
        id_dict={}
        answer={}
        if(validate(start_time) and validate(end_time)):
            start=datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
            end=datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
            with open('json_3.json') as f:
                J = json.load(f)
                L = []

                for item in J:
                    i=item['id']
                    s=0
                    if(item['state']):
                        s=1
                    b1=item['belt1']
                    b2=item['belt2']
                    t=datetime.strptime(item['time'], '%Y-%m-%d %H:%M:%S')
                    t=t.replace(tzinfo=timezone.utc)
                    L.append((t, int(remove_alphabets(i)), (1 - s) * b1, s * b2))
                    # print((t.time(), int(remove_alphabets(i)), (1 - s) * b1, s * b2))

                for item in L:
                    t = item[0]
                    i = item[1]
                    b1 = item[2]
                    b2 = item[3]
                    if t>=start and t<=end:
                        tmp = (0,0,0)
                        if i in id_dict:
                            tmp = id_dict[i]
                        id_dict[i] = (b1 + tmp[0], b2 + tmp[1], 1 + tmp[2])
                for key in id_dict:
                    tmp = id_dict[key]
                    answer[key] = (tmp[0]/tmp[2],tmp[1]/tmp[2])
        answer = sorted(answer.items())
        print(answer)
        l=[]
        for key in answer:
            dic={}
            dic["id"] = key[0]
            dic["avg_belt1"] = key[1][0]
            dic["avg_belt2"] = key[1][1]
            l.append(dic)

    return jsonify(l)
