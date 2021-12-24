import imghdr
import os
from website import create_app
from flask import render_template
from werkzeug import exceptions
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask import Flask, flash, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
from flask_login import current_user
import website.rooms as rooms
from website import db
from website.models import Game
import schedule
from threading import Thread
import time
global count
count = False

app = create_app()
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'website/static/pfp/'
app.config['UPLOAD_FOLDER'] = '/static'


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/user/<int:user_id>', methods=['POST'])
def upload_files(user_id):
    uploaded_file = request.files['pfp']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('profiles.profile', user_id=user_id))

socketio = SocketIO(app)
#handles 404 errors
@app.errorhandler(exceptions.NotFound)
def page_not_found(e):
    return render_template('404.html', user = current_user), 404

@socketio.on('draft')
def draft(game_id):
    join_room(game_id['data'])
    emit('detour', {'data': game_id['data']}, to=game_id['data'])

@socketio.on('valid')
def valid(game_id):
    valid_claims = rooms.get_valid_claims(game_id)
    is_turn = rooms.is_turn(game_id)
    round = db.session.query(Game).filter_by(id=game_id['data']).first().ticker
    emit("refresh", {'data': game_id['data'], 'claims': valid_claims, 'is_turn': is_turn, 'round': round})

@socketio.on('draft_leave')
def draft_leave(game_id):
    leave_room(game_id['data'])
    print("User left Room " + str(game_id['data']))

@socketio.on('empire')
def empire(game_id):
    join_room(game_id['data'])
    emit("broadcast", game_id, to=game_id["data"])

@socketio.on('updates')
def updates(game_id):
    empire_list = rooms.get_empire_list(game_id)
    emit("update", {'data': game_id['data'], 'empire_list': empire_list})

def run_mil():
    schedule.every(1).minutes.do(rooms.add_infantry_daily)
    while True:
        schedule.run_pending()
        time.sleep(1)

def threads_for_days():
    thread = Thread(target=run_mil, daemon=True)
    thread.start()

#makes it so it only runs the app if it is done specifically by this file
if __name__ == '__main__':
    threads_for_days()
    socketio.run(app, debug=False, host='localhost', port=5001, use_reloader=False) # http://localhost:5001/
    

