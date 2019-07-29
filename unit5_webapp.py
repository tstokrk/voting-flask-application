from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics
from collections import Counter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)


class Formdata(db.Model):
    __tablename__ = 'formdata'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    age = db.Column(db.Integer)
    income = db.Column(db.Integer)
    month = db.Column(db.Integer)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    q8 = db.Column(db.Integer)

    def __init__(self, gender, email, age, income, month, q1, q2, q3, q4, q5, q6, q7, q8):
        self.gender = gender
        self.email = email
        self.age = age
        self.income = income
        self.month = month
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q6 = q6
        self.q7 = q7
        self.q8 = q8


db.create_all()


@app.route("/")
def welcome():
    return render_template('welcome.html')


@app.route("/form")
def show_form():
    return render_template('form.html')


@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)


@app.route("/result")
def show_result():
    fd_list = db.session.query(Formdata).all()

    q1 = []
    q2 = []
    q3 = []

    for el in fd_list:
        q1.append(el.q1)
        q2.append(el.q2)
        q3.append(el.q3)

    q1 = Counter(q1).values()
    q2 = Counter(q2).values()
    q3 = Counter(q3).values()

    if len(q1) > 0:
        mean_q1 = statistics.mode(q1)
    else:
        mean_q1 = 0
    if len(q2) > 0:
        mean_q2 = statistics.mean(q2)
    else:
        mean_q2 = 0
    if len(q3) > 0:
        mean_q3 = statistics.mean(q3)
    else:
        mean_q3 = 0

    # Prepare data for google charts
    data = [['q1', mean_q1], ['q2', mean_q2], ['q3', mean_q3]]

    return render_template('result.html', data=data)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    gender = request.form['gender']
    email = request.form['email']
    age = request.form['age']
    income = request.form['income']
    month = request.form['month']
    q1 = request.form['q1']
    q2 = request.form['q2']
    q3 = request.form['q3']
    q4 = request.form['q4']
    q5 = request.form['q5']
    q6 = request.form['q6']
    q7 = request.form['q7']
    q8 = request.form['q8']
    # Save the data
    fd = Formdata(gender, email, age, income, month, q1, q2, q3, q4, q5, q6, q7, q8)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()
