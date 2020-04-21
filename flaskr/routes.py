from datetime import datetime
import threading, time
from flask import current_app as app
from flask import Blueprint, render_template, copy_current_request_context
import RPi.GPIO as GPIO

from flask_socketio import SocketIO, emit

socketio = SocketIO()

stop_event = threading.Event()
daemon = threading.Thread()
isDaemonStarted = False
status = "0"
secondsBetweenSensorRead = 10

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
        # TODO really need daemon?
        while not stop_event.is_set():
            time.sleep(secondsBetweenSensorRead)
    
    def button_callback(channel):
        print("Button was pushed!")
        global status
        status = "1"
        emit('daemonProcess', {'datetime': str(datetime.now()), 'name': name, 'status': status})

    global isDaemonStarted
    if action == 'START':
        if not isDaemonStarted:
            GPIO.setwarnings(False) # Ignore warning for now
            GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
            GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin 
            GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback, bouncetime=2000) # Setup event on pin 10 rising edge
            daemon.__init__(target=daemonProcess, args=(name, status, stop_event), daemon=True)
            daemon.start()
            isDaemonStarted = True
    else:
        GPIO.cleanup() # Clean up
        stop_event.set()
        daemon.join()
        stop_event.clear()
        isDaemonStarted = False
