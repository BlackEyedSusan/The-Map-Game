from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from . import db



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #this is how you handle forms, you can do some other special things with them
        #as well
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login successful!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Email not registered with this site.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email is already registered.', category='error')
        elif len(email) < 4:
            flash('Must have an email over 3 characters.', category='error')
        elif len(username) < 2:
            flash('The username must be at least 2 characters.', category='error')
        elif password1 != password2:
            flash('The passwords must match.', category='error')
        elif len(password1) < 7:
            flash('Must have a password over 7 characters.', category='error')
        else:
            #for example here, you generate a password hash so you cannot reverse engineer the password, which adds security
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'), pfp="/static/pfp/blank.png", admin="nope")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) #I haven't made remember user togglable yet,
            #but it wouldn't be too hard to add a checkbox here
            flash('Account created successfully.', category='success')
            return redirect(url_for('views.join_game'))
            
    return render_template('sign_up.html', user=current_user)