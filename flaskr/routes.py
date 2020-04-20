from datetime import datetime
import threading, time
from flask import current_app as app
from flask import Blueprint, render_template, copy_current_request_context

from flask_socketio import SocketIO, emit

socketio = SocketIO()

stop_event = threading.Event()
daemon = threading.Thread()
isDaemonStarted = False
status = "0"
secondsBetweenSensorRead = 2

view = Blueprint("view", __name__)

@view.route("/")
def homepage():
    return render_template("homepage.html")

@view.route("/settings")
def settings():
    return render_template("settings.html")

@socketio.on('handleDaemon')
def on_handleDaemon(data):
    name=data['name']
    action=data['action']

    @copy_current_request_context
    def daemonProcess(name, status, stop_event):
        while not stop_event.is_set():
            emit('daemonProcess', {'datetime': str(datetime.now()), 
            'name': name, 
            'status': status})
            time.sleep(secondsBetweenSensorRead)

    global isDaemonStarted
    if action == 'START':
        if not isDaemonStarted:
            daemon.__init__(target=daemonProcess, args=(name, status, stop_event), daemon=True)
            daemon.start()
            isDaemonStarted = True
    else:
        stop_event.set()
        daemon.join()
        stop_event.clear()
        isDaemonStarted = False
