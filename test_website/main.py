from website import create_app
from flask import render_template
from werkzeug import exceptions
from flask_socketio import SocketIO

app = create_app()
socketio = SocketIO(app)
#handles 404 errors
@app.errorhandler(exceptions.NotFound)
def page_not_found(e):
    return render_template('404.html'), 404

#makes it so it only runs the app if it is done specifically by this file
if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost', port=5001) # http://localhost:5001/