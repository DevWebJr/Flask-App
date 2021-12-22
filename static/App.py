from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/library'
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


@app.route('/employees')
def employees():
    all_data = Employee.query.all()
    return render_template("employees.html.twig", employees=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        employee = Employee(name, email, phone)
        db.session.add(employee)

        db.session.commit()
        flash("Employee Inserted Successfully")

        return redirect(url_for('employees'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        employee = Employee.query.get(request.form.get('id'))

        employee.name = request.form['name']
        employee.email = request.form['email']
        employee.phone = request.form['phone']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('employees'))


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    employee = Employee.query.get(id)
    
    db.session.delete(employee)
    
    db.session.commit()
    
    flash("Employee Deleted Successfull")

    return redirect(url_for('employees'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    