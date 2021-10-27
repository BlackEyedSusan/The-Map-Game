import imghdr
import os
from website import create_app
from flask import render_template
from werkzeug import exceptions
from flask_socketio import SocketIO
from flask import Flask, flash, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

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
    return render_template('404.html'), 404


#makes it so it only runs the app if it is done specifically by this file
if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost', port=5001) # http://localhost:5001/