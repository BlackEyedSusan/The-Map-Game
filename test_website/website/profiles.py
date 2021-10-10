from flask import Blueprint, abort, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from .models import Game, GamesJoined, User, Empires, Friends
import os
from werkzeug.utils import secure_filename
#import PIL
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
                redirect(url_for('profiles.profile', user_id=user_id))
        elif request.form.get("Remove Friend") == "Remove Friend":
            is_friends1 = Friends.query.filter_by(user1=user_id, user2=current_user.id).first()
            is_friends2 = Friends.query.filter_by(user2=user_id, user1=current_user.id).first()
            if is_friends1 != None:
                db.session.delete(is_friends1)
            if is_friends2 != None:
                db.session.delete(is_friends2)
            db.session.commit()
            flash('User removed from friends.', category='neutral')
            redirect(url_for('profiles.profile', user_id=user_id))
        elif request.form.get("upload_pfp") == "upload_pfp":
            #photos = UploadSet('photos', IMAGES)
            #filename = photos.save(request.files['photo'])
            #rec = Photo(filename=filename, user=g.user.id)
            #rec.store()
            #flash("Photo saved.")
            #uploaded_file = request.files['file']
            #filename = secure_filename(uploaded_file.filename)
            #if filename != '':
                #file_ext = os.path.splitext(filename)[1]
                #if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    #abort(400)
                #uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            if 'pfp' not in request.files:
                flash('No file part', 'error')
                return redirect(request.url)
            file = request.files['pfp']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name = 'a' + str(user_id) + '.png'
                file.save(os.path.join('/static/pfp/', name))
            user_changed = db.session.query(User).filter_by(id=current_user.id).first()
            user_changed.pfp = f'/static/pfp/{filename}'
            db.session.commit()
            flash('Profile picture changed!', category='success')
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