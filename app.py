from datetime import datetime
from typing import Sequence
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import DefaultMeta
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class comment(db.Model):
    sr_no = db.Column(db.Integer, primary_key = True)
    desc = db.Column(db.String(300), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sr_no} - {self.title}'



@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = comment(title=title , desc=desc)
        db.session.add(todo)
        db.session.commit()
    show = comment.query.all()
    return render_template('index.html', show=show)

@app.route("/update/<int:sr_no>", methods=['GET','POST'])
def update(sr_no):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        upda = comment.query.filter_by(sr_no=sr_no).first()
        upda.title = title
        upda.desc = desc
        db.session.add(upda)
        db.session.commit()
        return redirect("/")
        
    upda = comment.query.filter_by(sr_no=sr_no).first()
    return render_template('update.html', upda=upda)

@app.route('/delete/<int:sr_no>')
def delete(sr_no):
    dele = comment.query.filter_by(sr_no=sr_no).first()
    db.session.delete(dele)
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=False)