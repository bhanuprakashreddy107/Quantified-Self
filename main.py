from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask,request,jsonify
from  flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from jinja2 import Template
from smtplib import SMTP
from celery import Celery
from celery.schedules import crontab
from flask_caching import Cache
import time




email =  'boyapallib@gmail.com'
password = 'keya amyk jblf tyez'
user_name = 'None'
app=Flask(__name__)
cache = Cache()

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///project.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["CACHE_TYPE"]="RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/2"
app.config["CACHE_DEFAULT_TIMEOUT"] = 1000

cache.init_app(app)
CORS(app)

db=SQLAlchemy(app)

#making celery app

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://localhost:6379',
    'result_backend': 'redis://localhost:6379',
})

celery = make_celery(app)



class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name=db.Column(db.String,nullable=False)
    user_email=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)

class Trackers(db.Model):
    tracker_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    tracker_name=db.Column(db.String,nullable=False)
    tracker_des = db.Column(db.String,nullable=False)
    format=db.Column(db.String,nullable=False)
    tuser = db.Column(db.String,nullable=False)

    # def __init__(self,tracker_name,format,tuser):
    #     self.tracker_name=tracker_name
    #     self.format = format
    #     self.tuser = tuser


class Logs(db.Model):
    log_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    log_value = db.Column(db.String,nullable=False)
    log_stamp= db.Column(db.String,nullable=False)
    log_note = db.Column(db.String,nullable=False)
    tid = db.Column(db.Integer,nullable=False)

@app.route('/addUser',methods=['POST'])
def addUser():
    if request.method == 'POST':
        user_name = request.json['user_name']
        user_email = request.json['user_email']
        password = request.json['password']
        u1 = Users(user_name = user_name, user_email=user_email,password = password)
        db.session.add(u1)
        db.session.commit()
        return jsonify({
            'status':'successfull'
        })

@app.route('/checkUser',methods=['POST'])
def checkUser():
    if request.method == 'POST':
        email = request.json['user_email']
        password = request.json['password']
        e1=Users.query.filter_by(user_email=email).first()
        e2=Users.query.filter_by(password=password).first()
        
        if(e1 is None or e2 is None):
            return jsonify({'confirm':'invalid'})
        elif (e1.id==e2.id):
            global user_name
            user_name = e1.user_name
            return jsonify({'confirm':'valid'})
        
        else:
            return jsonify({'confirm':'invalid'})
    
@app.route('/addTracker',methods=['POST'])
def addTracker():
    if request.method == 'POST':
        tracker_name = request.json['name']
        des = request.json['des']
        tracker_format = request.json['format']
        tuser = user_name
        t1 = Trackers(tracker_name = tracker_name,tracker_des = des,format = tracker_format,tuser=tuser)
        db.session.add(t1)
        db.session.commit()
        t = Trackers.query.filter_by(tracker_name = tracker_name).first()
        return jsonify({
            'confirm':'successfull',
            'id':str(t.tracker_id)
        })

@app.route('/seeTrackers',methods=['POST'])
def seeTrackers():
    if request.method == 'POST':
        trackers = Trackers.query.filter_by(tuser = user_name).all()
        d=[]
        for tracker in trackers:
            d.append({
                'tracker_name':str(tracker.tracker_name),
                'format':str(tracker.format),
                'des':str(tracker.tracker_des),
                'tuser':str(tracker.tuser),
                'tracker_id':str(tracker.tracker_id)
            })
        return jsonify(d)

@app.route('/getUser',methods=['POST'])
def getUser():
    if request.method == 'POST':
        if user_name != 'None':
            user = Users.query.filter_by(user_name = user_name).first()
            return jsonify({'name':str(user.user_name)})
        else:
            return jsonify({'name':'None'})

@app.route('/removeUser',methods=['POST'])
def logout():
    if request.method == 'POST':
        global user_name
        user_name = 'None'
        return jsonify({'confirm':'success'})

@app.route('/addLog/<string:t_id>',methods=['POST'])
def addLog(t_id):
    if request.method == 'POST':
        value = request.json['log_value']
        note = request.json['log_note']
        l=time.localtime()
        s=''
        if len(str(l.tm_min)) !=2 :
            p = '0' + str(l.tm_min)
        else:
            p = str(l.tm_min)
        if len(str(l.tm_hour)) !=2:
            m = '0' + str(l.tm_hour)
        else:
            m = str(l.tm_hour)
        if len(str(l.tm_mon)) !=2:
            month = '0' + str(l.tm_mon)
        else:
            month = str(l.tm_mon)
        s=s+str(l.tm_year)+'-'+str(month)+'-'+str(l.tm_mday)+str('    ')+m+':'+p+':'+str(l.tm_sec)
        l = Logs( log_value = value , log_stamp = s ,log_note = note, tid = t_id )
        db.session.add(l)
        db.session.commit()
        return jsonify({
            'confirm' : 'yes'
        })

@app.route('/deleteTracker/<string:t_id>',methods=['DELETE'])
def deleteTracker(t_id):
    if request.method == 'DELETE':
        ts = Trackers.query.filter_by(tracker_id = int(t_id)).first()
        ls = Logs.query.filter_by(tid=int(t_id)).all()
        db.session.delete(ts)
        for i in ls:
            db.session.delete(i)
        db.session.commit()
        return jsonify({
            'confirm':'success'
        })

@app.route('/deleteLog/<string:l_id>',methods=['DELETE'])
def deleteLog(l_id):
    if request.method == 'DELETE':
        l = Logs.query.filter_by(log_id=int(l_id)).first()
        db.session.delete(l)
        db.session.commit()
        return jsonify({
            'confirm':'success'
        })

@app.route('/viewData/<string:t_id>',methods=['POST'])

def viewData(t_id):
    if request.method == 'POST':
        ls = Logs.query.filter_by(tid=int(t_id)).all()
        l=[]
        for log in ls:
            l.append({
                'log_id':str(log.log_id),
                'log_value':str(log.log_value),
                'log_stamp':str(log.log_stamp),
                'log_note':str(log.log_note),
                'tid':str(log.tid)
            })
        l.reverse()
        return jsonify(l)

@app.route('/getData/<string:t_id>',methods=['POST'])

def getData(t_id):
    if request.method == 'POST':
        ls = Logs.query.filter_by(tid=int(t_id)).all()
        ts = Trackers.query.filter_by(tracker_id=int(t_id)).first()
        ty = ts.format
        labels=[]
        values=[]
        if ty == 'Numerical':
            for log in ls:
                labels.append(int(str((log.log_stamp)[8:10])))
                try:
                    values.append(int(log.log_value))
                except:
                    values.append(log.log_value)
            l = {'labels':labels,'values':values}
        elif ty == 'Time Duration':
            for log in ls:
                labels.append(int(str(log.log_stamp)[8:10]))
                values.append(int(log.log_value[0:2])*60+int(log.log_value[6:8]))
            l={'labels':labels,'values':values}
        elif ty == 'Boolean':
            for log in ls:
                labels.append(int(str(log.log_stamp)[8:10]))
                if log.log_value == 'Yes':
                    values.append(1)
                else:
                    values.append(0)
            l = {'labels':labels,'values':values}

        return jsonify(l)

@app.route('/saveTracker/<string:t_id>',methods=['POST'])
def saveTracker(t_id):
    if request.method == 'POST':
        t_name = request.json['name']
        des = request.json['des']
        t_type = request.json['type']

        l = Logs.query.filter_by(tid=int(t_id)).all()
        d = Trackers.query.filter_by(tracker_id=int(t_id)).first()
        if str(d.format) == str(t_type):
            db.session.delete(d)
            t1 = Trackers(tracker_name = t_name,tracker_des=des,format= t_type,tuser = user_name)
            db.session.add(t1)
            db.session.commit()
            t = Trackers.query.filter_by(tracker_name = t_name).first()
            id = t.tracker_id
            for log in l:
                p = Logs( log_value = log.log_value , log_stamp = log.log_stamp ,log_note = log.log_note, tid = id)
                db.session.add(p)
            for log in l:
                db.session.delete(log)
            db.session.commit()
        else:
            db.session.delete(d)
            t1 = Trackers(tracker_name = t_name,tracker_des=des,format= t_type,tuser = user_name)
            db.session.add(t1)
            for log in l:
                db.session.delete(log)
            db.session.commit()
        return jsonify({
                'confirm':'success'
            })

@app.route('/saveLog/<string:l_id>',methods=['POST'])
def saveLog(l_id):
    if request.method == 'POST':
        value = request.json['log_value']
        note = request.json['log_note']
        

        p = Logs.query.filter_by(log_id=int(l_id)).first()
        if value=='':
            value = p.log_value
        id=p.tid
        db.session.delete(p)
        l=time.localtime()
        s=''
        if len(str(l.tm_min)) !=2 :
            p = '0' + str(l.tm_min)
        else:
            p = str(l.tm_min)
        if len(str(l.tm_hour)) !=2:
            m = '0' + str(l.tm_hour)
        else:
            m = str(l.tm_hour)
        if len(str(l.tm_mon)) !=2:
            month = '0' + str(l.tm_mon)
        else:
            month = str(l.tm_mon)
        s=s+str(l.tm_year)+'-'+str(month)+'-'+str(l.tm_mday)+str('    ')+m+':'+p+':'+str(l.tm_sec)
        l = Logs(log_value = value,log_stamp =s,log_note=note,tid=id )
        db.session.add(l)
        db.session.commit()
        return jsonify({
            'confirm':'success'
        })

@app.route('/getType/<string:t_id>',methods=['POST'])
def getType(t_id):
    if request.method == 'POST':
        t = Trackers.query.filter_by(tracker_id=int(t_id)).first()
        return jsonify({
            'type':str(t.format)
        })

@app.route('/forgot',methods=['POST'])
def forgot():
    if request.method == 'POST':
        email = request.json['email']
        new_pass = request.json['new_pass']
        c_pass = request.json['c_pass']

        user = Users.query.filter_by(user_email = email).first()
        if email=='' or new_pass=='' or c_pass == '':
            return jsonify({
                'response' : 'Null'
            })

        if user == None:
            return jsonify({
                'response' : 'invalidEmail'
            })
        old = user.password
        if new_pass != c_pass:
            return jsonify({
                'response':'dontMatch'
            })
        if new_pass == old:
            return jsonify({
                'response':'sameOldAndNew'
            })
        name = user.user_name
        i = user.id
        db.session.delete(user)
        adduser = Users(id = i,user_name = name,user_email = email,password = new_pass)
        db.session.add(adduser)
        db.session.commit()
        return jsonify({
            'response' : 'success'
        })
        
        

@app.route('/download',methods=['POST'])

def download():
    if request.method == 'POST':
        ts = Trackers.query.filter_by(tuser = user_name).all()
        # [slno,'tracker_name','average_value','no of logs',total value]
        li=[]
        n = 1
        for tracker in ts:
            s = 0
            count = 0
            yes=0
            ls = Logs.query.filter_by(tid = tracker.tracker_id).all()
            if tracker.format == 'Numerical':
                for log in ls:
                    s += int(log.log_value)
                    count += 1
                if count > 0:
                    p={'n':n,'tracker':tracker.tracker_name,'count':count,'avg':s/count,'total':s}
                else:
                    p={'n':n,'tracker':tracker.tracker_name,'count':0,'avg':0,'total':0}
                li.append(p)
            elif tracker.format == 'Boolean':
                for log in ls:
                    if log.log_value=='Yes':
                        yes += 1
                    count += 1
                if count > 0:
                    p={'n':n,'tracker':tracker.tracker_name,'count':yes,'avg':(yes)/count,'total':count}
                else:
                    p={'n':n,'tracker':tracker.tracker_name,'count':0,'avg':0,'total':0}
                li.append(p)
            elif tracker.format == 'Time Duration':
                for log in ls:
                    val = int(log.log_value[0:2])*60 + int(log.log_value[6:8])
                    s += val
                    count += 1
                if count > 0:
                    p={'n':n,'tracker':tracker.tracker_name,'count':count,'avg':s/count,'total':s}
                else:
                    p={'n':n,'tracker':tracker.tracker_name,'count':0,'avg':0,'total':0}
                li.append(p)
            n += 1

        return jsonify(li)


def getReportData(trackers):
    presentMonth = int(time.localtime().tm_mon)
    previous = presentMonth
    new = []
    old=[]
    for tracker in trackers:
        l=[]
        logData = Logs.query.filter_by(tid = tracker.tracker_id).all()
        s = 0
        count = 0
        yes_count = 0
        no_count = 0
        for log in logData:
            if int(log.log_stamp[5:7]) == previous:
                l.append(log)
        if tracker.format == 'Numerical':
            for log in l:
                s += int(log.log_value)
                count += 1
            if count > 0:
                new.append([tracker.tracker_name,'Numerical',s,count,s/count])
            else:
                old.append(tracker.tracker_name)
        elif tracker.format == 'Boolean':
            for log in l:
                if log.log_value == 'Yes':
                    yes_count += 1
                else:
                    no_count += 1
                count += 1
            if count > 0:
                new.append([tracker.tracker_name,'Boolean',yes_count,yes_count/count,count])
            else:
                old.append(tracker.tracker_name)
        else:
            for log in l:
                val = int(log.log_value[0:2])*60 + int(log.log_value[6:8])
                s += val
                count += 1
                if count > 0:
                    new.append([tracker.tracker_name,'Time Duration',s,count,s/count])
                else:
                    old.append(tracker.tracker_name)
    return [old,new]

        

@app.route('/getRecent',methods=['POST'])

def getRecent():
    ts = Trackers.query.filter_by(tuser=user_name).all() 
    d={}
    v=0
    for tracker in ts:
        ls = Logs.query.filter_by(tid=tracker.tracker_id).all()
        for log in ls:
            new = log
            v=1
        
        if v==1:
            d[tracker.tracker_id] = {'recentl':new.log_stamp,'recentv':log.log_value}
        else:
            d[tracker.tracker_id] = {'recentl':'Nothing added','recentv':'no value'}
        v=0

    return jsonify(d)

@cache.cached(timeout=40)
def getrecenttime(user):
    ts = Trackers.query.filter_by(tuser=user).all() 
    d=[]
    v=0
    for tracker in ts:
        ls = Logs.query.filter_by(tid=tracker.tracker_id).all()
        for log in ls:
            new = log
            v=1
        
        if v==1:
            d.append({'name':tracker.tracker_name,'recentl':new.log_stamp,'recentv':log.log_value})
        else:
            d.append({'name':tracker.tracker_name,'recentl':0,'recentv':0})
        v=0
    return d






#<-------------------------------------------------------------------------------------------------------------->
#<-------------------------------------------------ONLY celery Tasks-------------------------------------------->
#<-------------------------------------------------------------------------------------------------------------->


@celery.on_after_configure.connect
def setup_periodic_emails(sender, **kwargs):
    sender.add_periodic_task(crontab(),send.s(),name = 'check every 4 hours')


@celery.on_after_configure.connect
def setup_report(sender,**kwargs):
    sender.add_periodic_task(crontab(),pdfSend.s(),name="sending monthly report")

@celery.task(name='main.send')
def send():
    

    allusers = Users.query.all()
    for user in allusers:
        
        d = getrecenttime(user.user_name)
        for tracker in d:
            t = time.localtime()
            if tracker['recentl'] != 0:
                hours = t.tm_hour
                h = int(tracker['recentl'][14:16])
                if(hours - h >= 24):
                    # msg.set_content("please add log to {0} its more than 24 hours since you added a log".format(tracker['name']))
                    # server.send_message(msg)
                    with open('./alert.html','r') as f:
                        tem = Template(f.read())
                    send_alert(user.user_email,tem.render(tracker=tracker['name']))
                    print('Mail sent')
                else:
                    print('No need for mail')
            else:
                with open('./alert.html','r') as f:
                        tem = Template(f.read())
                send_alert(user.user_email,tem.render(tracker=tracker['name']))
                print('Mail sent')

@celery.task(name="main.pdfSend")
def pdfSend():
    allusers = Users.query.all()
    for user in allusers:
        ts = Trackers.query.filter_by(tuser = user.user_name).all()
        [old,new] = getReportData(ts)
        with open('./report.html', 'r') as f:
            tem = Template(f.read())
        send_mail(user.user_email,tem.render(old=old,new=new,user=user.user_name))

    
def send_mail(user,message):
    msg = MIMEMultipart()
    msg['Subject'] = 'Trackers Monthly Report'
    msg['From'] = email
    msg['To']=user

    server = SMTP('smtp.gmail.com',525)
    server.starttls()

    msg.attach(MIMEText(message,'html'))
    server.login(email,password)
    server.send_message(msg)
    server.quit()

def send_alert(em,message):
    msg = MIMEMultipart()
    server = SMTP('smtp.gmail.com',525)
    server.starttls()

    msg['Subject'] = 'add log'
    msg['From'] = email
    msg['To']=em
    

    server.login(email,password)
    
    msg.attach(MIMEText(message,'html'))
    server.send_message(msg)
    server.quit()


if __name__ == "__main__":
    app.run(debug=True)