# -*- coding:utf-8 -*-
import os
import psycopg2

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'z19Q(*@&#(hf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True

manager = Manager(app)
db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    location = db.Column(db.Integer, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    location = db.Column(db.Integer, unique=True)
    items = db.relationship('Item', backref='category', lazy='dynamic')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        body = request.form.get('item')
        id = request.form.get('category')
        category = Category.query.get_or_404(id)
        item = Item(body=body, category=category)
        db.session.add(item)
        return redirect(url_for('category', id=id))
    return redirect(url_for('category', id=1))


@app.route('/category/<int:id>', methods=['GET', 'POST'])
def category(id):
    category = Category.query.get_or_404(id)
    categories = Category.query.all()
    items = category.items
    return render_template('index.html', items=items,
                           categories=categories, category_now=category)


