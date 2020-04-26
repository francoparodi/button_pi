from datetime import datetime
import threading, time
from flask import current_app as app
from flask import Blueprint, render_template, redirect, url_for, copy_current_request_context

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import sys
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
    sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)
    import RPi.GPIO as GPIO
    import smbus

from flask_socketio import SocketIO, emit

socketio = SocketIO()

stop_event = threading.Event()
daemon = threading.Thread()
isDaemonStarted = False
secondsBetweenGPIOStatus = 1
gPIOEvent = False
dictEvents = {'10': 0, '18': 0}

view = Blueprint("view", __name__)

@view.route("/")
def homepage():
    return render_template("homepage.html")

@view.route('/increment/<int:channel>')
def incrementScore(channel):
    dictEvents[str(channel)] = dictEvents[str(channel)] + 1
    on_connect()
    return redirect(url_for("view.homepage"))

@view.route('/decrement/<int:channel>')
def decrementScore(channel):
    dictEvents[str(channel)] = dictEvents[str(channel)] - 1
    on_connect()
    return redirect(url_for("view.homepage"))

@view.route("/reset")
def reset():
    dictEvents['10'] = 0
    dictEvents['18'] = 0
    on_connect()
    return redirect(url_for("view.homepage"))

@socketio.on('connect')
def on_connect():
    name='name'
    channel10 = dictEvents['10']
    channel18 = dictEvents['18']
    socketio.emit('daemonProcess', {'datetime': str(datetime.now()), 'name': name, 'channel10': str(channel10), 'channel18': str(channel18)})

@socketio.on('handleDaemon')
def on_handleDaemon(data):
    global gPIOEvent
    name=data['name']
    action=data['action']

    @copy_current_request_context
    def daemonProcess(name, stop_event):
        # Daemon needed cause emit from button_callback is not allowed
        global gPIOEvent
        while not stop_event.is_set():
            if gPIOEvent:
                channel10 = dictEvents['10']
                channel18 = dictEvents['18']
                socketio.emit('daemonProcess', {'datetime': str(datetime.now()), 'name': name, 'channel10': str(channel10), 'channel18': str(channel18)})
                gPIOEvent = False
            time.sleep(secondsBetweenGPIOStatus)
    
    def button_callback(channel):
        print("Event on channel #" + str(channel))
        global gPIOEvent
        gPIOEvent = True
        dictEvents[str(channel)] = dictEvents[str(channel)] + 1

    global isDaemonStarted
    if action == 'START':
        if not isDaemonStarted:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
            GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin 
            GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback, bouncetime=2000) # Setup event on pin 10 rising edge
            GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 18 to be an input pin 
            GPIO.add_event_detect(18,GPIO.RISING,callback=button_callback, bouncetime=2000) # Setup event on pin 18 rising edge
            
            daemon.__init__(target=daemonProcess, args=(name, stop_event), daemon=True)
            daemon.start()
            gPIOEvent = False
            isDaemonStarted = True
    else:
        GPIO.cleanup()
        stop_event.set()
        daemon.join()
        stop_event.clear()
        gPIOEvent = False
        isDaemonStarted = False
