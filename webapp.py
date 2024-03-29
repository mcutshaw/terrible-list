#!/usr/bin/python3
from datetime import datetime
from configparser import ConfigParser
from flask import Flask, render_template, request, Response, session, redirect, url_for, flash
from functools import wraps
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from os import urandom
import subprocess

from db import db
from user import User
from forms import LoginForm, RegisterForm, RemoveForm, AddForm

app = Flask(__name__)      
SECRET_KEY = urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

config = ConfigParser()
config.read('list.conf')

db = db(config)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    if _auth(user_id):
        return User(user_id)
    else:
        return None

def _auth(username):
    process = subprocess.Popen(f"getent passwd | grep {username}",stdout=subprocess.PIPE, shell=True)
    process.communicate()
    return process.returncode == 0

def auth(username, password):
    if _auth(username):
        return True
    else:
        return False

@app.route('/',methods=["GET"])
def root():
    return redirect(url_for('login'))

@app.route('/login',methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('thelist'))
    form = LoginForm()
    if form.validate_on_submit():
        if auth(form.username.data, form.password.data):
            user = User(form.username.data)
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('register'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register',methods=["POST","GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print('validated')
        try:
            subprocess.Popen(f"echo {form.password.data} | sudo pw useradd {form.name.data} -s /usr/local/bin/bash -G wheel -h 0",stdout=subprocess.PIPE, shell=True)
            return redirect(url_for('login'))
        except:
            print('excepted')
            flash('ERROR')
            return redirect(url_for('register'))
    else:
        print(form.errors)

    return render_template('register.html', title='Register', form=form)

@login_required
@app.route('/list',methods=["POST","GET"])
def thelist():
    return render_template('thelist.html', title='List', users=db.getAllPersons())

@app.route('/about',methods=["POST","GET"])
def about():
    return render_template('about.html', title='About')

@login_required
@app.route('/add',methods=["POST","GET"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        print('validated')
        try:
            if form.status.data:
                status_text = "NAUGHTY"
            else:
                status_text = "NICE"
            db.insertPerson(form.username.data, form.name.data, status=status_text, status_description=form.status_description.data)
            return redirect(url_for('add'))
        except:
            print('excepted')
            flash('ERROR')
            return redirect(url_for('add'))
    else:
        print(form.errors)

    return render_template('add.html', title='Add', form=form)

@login_required
@app.route('/remove',methods=["POST","GET"])
def remove():
    form = RemoveForm()
    if form.validate_on_submit():
        print('validated')
        try:
            db.deletePersonByUsername(form.name.data)
            return redirect(url_for('remove'))
        except Exception as e:
            print(e)
            flash('ERROR')
            return redirect(url_for('remove'))
    else:
        print(form.errors)

    return render_template('remove.html', title='Remove', form=form)
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
