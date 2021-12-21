from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3306/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))    
    email = db.Column(db.String(255))    
    phone = db.Column(db.String(255))    
    
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))  

    def __init__(self, name):
        self.name = name
        self.books = db.relationship('Book', backref='owner')
        
        
class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))    
    price = db.Column(db.Float)    
    category = db.Column(db.Integer, db.ForeignKey('category.id'))    

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


@app.route('/')
def index():
    return render_template("index.html.twig")


@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Employee(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
    