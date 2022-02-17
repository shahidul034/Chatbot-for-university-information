from flask import Flask, redirect,render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import random
import logging
import sys
import numpy
from scipy import stats

def central_of_tendency(li):
    li=li.split(" ")
    li=[int(x) for x in li]
    mean = numpy.mean(li)
    median = numpy.median(li)
    mode = stats.mode(li)
    std_dev=x = numpy.std(li)
    return "mean: "+str(mean)," median: ",str(median)," mode: ",str(mode)," standard deviation: ",str(std_dev)+" variance: "+str(std_dev*std_dev)

def five_num_sum(li):
    li=li.split(" ")
    li=[int(x) for x in li]
    from numpy import percentile
    from numpy.random import rand
    data = numpy.array(li)
    quartiles = percentile(data, [25, 50, 75])
    data_min, data_max = data.min(), data.max()
    five_num="Min: "+str(data_min)+" Q1: "+str(quartiles[0])+" Median: "+ str(quartiles[1])+" Q3: "+str(quartiles[2])+" Max: "+str(data_max)
    return five_num
    

def mydata():
    
    d=[]
    for x in range(1,10+1):
        d.append(str(random.randint(1,100)))
    return ' '.join(d)
    

file_path = os.path.abspath(os.getcwd())+"\\todo.db"
print(file_path)
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

db=SQLAlchemy(app) 
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
@app.route("/",methods=['GET','POST'])
def hello_world():
    title2=""
    desc2=""
    date_created2=""
    if request.method =='POST':
        title2=(request.form['title'])
        dat=Todo.query.all()
        flag=1
        for x in dat:
            if title2==x.title:
                flag=0
                print("already exist!!!")
                break
        if flag:
            desc2=mydata() #changes in this portion
            todo=Todo(title=title2,desc=desc2)
            db.session.add(todo)
            db.session.commit()
            print("inserted item successfully")
        
    allTodo=Todo.query.all()
    for x in allTodo:
        if x.title==title2:
            desc2=x.desc
            title2=x.title
            date_created2=x.date_created
            break
    answer=""
    five_num=""
    import datetime
    time= datetime.datetime.now()
    if len(desc2)>=5:
        answer=(central_of_tendency(desc2))
        five_num=five_num_sum(desc2)
    else:
        answer="(Answer will be published at 4 pm) "+str(time)
        
        

    return render_template("index.html",title=title2,desc=desc2,ans=answer,five_num=five_num)

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=(request.form['title'])
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        print("Updated item successfully")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)

@app.route("/about")
def about():
    return "<h1>Md. Shahidul Salim (Shakib)<br>Lecturer,CSE,Uttara University"
 
@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    print("deleted successfully")
    return redirect("/")
    


if __name__ == "__main__":
    app.run(debug=True)