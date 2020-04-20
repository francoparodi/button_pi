from flask import Flask, render_template

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'secret!'

    from flaskr.routes import socketio
    socketio.init_app(app)

    from flaskr.routes import view
    app.register_blueprint(view)

    return app