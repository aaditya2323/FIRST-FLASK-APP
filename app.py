from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///list.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class TodoList(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo=TodoList(title=title,desc= desc)
        db.session.add(todo)
        db.session.commit()
    todo=TodoList.query.all()
    return render_template("index.html",todos=todo)

@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo =TodoList.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    alltodo =TodoList.query.filter_by(sno=sno).first()
    return render_template("update.html",todos=alltodo)
    
    

@app.route('/delete/<int:sno>')
def delete(sno):
    alltodo =TodoList.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")
   






if __name__ == "__main__": 
   
    app.run(debug=True)
