import os
from website import create_app
from flask import render_template
from werkzeug import exceptions
from flask_socketio import SocketIO
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

app = create_app()
socketio = SocketIO(app)
#handles 404 errors
@app.errorhandler(exceptions.NotFound)
def page_not_found(e):
    return render_template('404.html'), 404
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#makes it so it only runs the app if it is done specifically by this file
if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost', port=5001) # http://localhost:5001/