from flaskr import create_app
from flaskr.routes import socketio

application = create_app()

if __name__ == "__main__":
    socketio.run(application, debug=True)