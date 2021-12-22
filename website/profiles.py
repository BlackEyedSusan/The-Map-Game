from flask import Blueprint, abort, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from .models import Game, GamesJoined, StatsAllTime, User, Empires, Friends
import os
from PIL import Image
from werkzeug.utils import secure_filename
from . import db

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
                flash('User addded to friends!', category='success')
                return redirect(url_for('profiles.profile', user_id=user_id))
        elif request.form.get("Remove Friend") == "Remove Friend":
            is_friends1 = Friends.query.filter_by(user1=user_id, user2=current_user.id).first()
            is_friends2 = Friends.query.filter_by(user2=user_id, user1=current_user.id).first()
            if is_friends1 != None:
                db.session.delete(is_friends1)
            if is_friends2 != None:
                db.session.delete(is_friends2)
            db.session.commit()
            flash('User removed from friends.', category='neutral')
            return redirect(url_for('profiles.profile', user_id=user_id))
        elif request.form.get("upload_pfp") == "upload_pfp":
            uploaded_file = request.files['pfp']
            if uploaded_file.filename == '':
                flash("You have to upload a file to change your profile picture.", category='error')
                return redirect(url_for('profiles.profile', user_id=user_id))
            filename = str(current_user.id) + ".png"
            uploaded_file.save(os.path.join('website/static/pfp/', filename))
            image = Image.open(f'website/static/pfp/{filename}')
            image = image.resize((256,256))
            image.save(f'website/static/pfp/{filename}')
            cur_user = db.session.query(User).filter_by(id=current_user.id).first()
            cur_user.pfp = f'/static/pfp/{filename}'
            db.session.commit()

            return redirect(url_for('upload_files', user_id=user_id))

            
    user = User.query.filter_by(id=user_id).first()
    counter=0
    is_friends = False
    is_friends1 = Friends.query.filter_by(user1=user_id, user2=current_user.id).first()
    is_friends2 = Friends.query.filter_by(user2=user_id, user1=current_user.id).first()
    if is_friends1 != None or is_friends2 != None:
        is_friends = True
    for games in db.session.query(GamesJoined).filter_by(user=user_id):
        counter += 1
    if user == current_user:
        is_current_user = True
    else:
        is_current_user = False
    stats = db.session.query(StatsAllTime).filter_by(user=user_id).first()
    return render_template('profile.html', is_current=is_current_user, user=current_user, player=user, games_joined=counter,
                             is_friends=is_friends, stats=stats)

@login_required
@profiles.route('friends')
def friends():
    result_list = []
    friends_list = []
    for friend in db.session.query(Friends).filter_by(user1=current_user.id):
        friends_list.append(friend.user2)
        print('worked 1')
    for friend in db.session.query(Friends).filter_by(user2=current_user.id):
        friends_list.append(friend.user1)
        print('worked 2')
    for friend in friends_list:
        print('worked 3')
        result = db.session.query(User).filter_by(id=friend).first()
        result_list.append([result, url_for('profiles.profile', user_id=result.id)])
    return render_template('friends.html', user=current_user, friends=result_list)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS