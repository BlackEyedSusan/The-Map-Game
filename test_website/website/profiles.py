from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from .models import Game, GamesJoined, User, Empires, Friends
from . import db
import sqlite3 as dbapi
import json

profiles = Blueprint('profiles', __name__)

@profiles.route('<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    if request.method == 'POST':
        if request.form.get("Add Friend") == "Add Friend":
            new_friend = Friends(user1=user_id, user2=current_user.id)
            is_friends = False
            is_friends1 = Friends.query.filter_by(user1=user_id, user2=current_user.id).first()
            is_friends2 = Friends.query.filter_by(user2=user_id, user1=current_user.id).first()
            if is_friends1 != None or is_friends2 != None:
                is_friends = True
            if is_friends == True:
                flash('You are already friends with this user.', category='error')
            else:
                db.session.add(new_friend)
                db.session.commit()
                flash('User addded to friends!', category='error')
                redirect(url_for('profiles.profile', user_id=user_id))
        elif request.form.get("Remove Friend") == "Remove Friend":
            is_friends1 = Friends.query.filter_by(user1=user_id, user2=current_user.id).first()
            is_friends2 = Friends.query.filter_by(user2=user_id, user1=current_user.id).first()
            if is_friends1 != None:
                db.session.delete(is_friends1)
            if is_friends2 != None:
                db.session.delete(is_friends2)
            db.session.commit()
            flash('User removed from friends.', category='success')
            redirect(url_for('profiles.profile', user_id=user_id))
            
    user = User.query.filter_by(id=user_id).first()
    counter=0
    is_friends = False
    is_friends1 = Friends.query.filter_by(user1=user_id, user2=current_user.id).first()
    is_friends2 = Friends.query.filter_by(user2=user_id, user1=current_user.id).first()
    if is_friends1 != None or is_friends2 != None:
        is_friends = True
    for games in GamesJoined.query.filter_by(id=user_id):
        counter += 1
    if user == current_user:
        is_current_user = True
    else:
        is_current_user = False
    return render_template('profile.html', is_current=is_current_user, user=current_user, player=user, games_joined=counter, is_friends=is_friends)