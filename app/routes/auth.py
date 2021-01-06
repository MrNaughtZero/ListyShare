from flask import Flask, Blueprint, render_template, redirect, url_for, request, abort, flash, get_flashed_messages
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.forms import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/auth/register', methods=['GET'])
def register():
    return render_template('/auth/register.html', form=RegisterForm(), message=get_flashed_messages())

@auth_bp.route('/auth/create/account', methods=['POST'])
def register_account():
    form = RegisterForm()

    if not form.validate_on_submit():
        flash(list(form.errors.values())[0])
        return redirect(url_for('auth.register'))
    
    usr = User(username=request.form.get('username'), email=request.form.get('email'), password=User().hash_password(request.form.get('password'))).create_user()

    login_user(usr)
    return redirect(url_for('main.profile'))

@auth_bp.route('/auth/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template('/auth/login.html', message=get_flashed_messages(), form=LoginForm())

@auth_bp.route('/auth/login/attempt', methods=['POST'])
def login_attempt():
    query = User().login_attempt(request.form.get('username'), request.form.get('password'))
    
    if not query:
        flash('Incorrect Login Details')
        return redirect(url_for('auth.login'))
    
    login_user(query)
    
    return redirect(url_for('main.profile'))

@auth_bp.route('/auth/logout', methods=['GET'])
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    logout_user()
    return redirect(url_for('auth.login'))