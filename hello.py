from flask import Flask, render_template, request
from flask_socketio import SocketIO
from raspberryController.model.raspberry import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8080)
    # app.run(host='0.0.0.0', port=8080, debug=True)
    
@app.route("/")
def hello():
    return "Python Flask Hello!"

@app.route("/command/")
def command():
    bar = request.args.to_dict();
    left = bar['left']
    move = bar['move']
    duration = bar['duration']  
    try:
        left = int(left)
        duration = int(duration)
        move = int(move)
    except ValueError:
        return "Parameters must be a INT"
    
    # if right or left is not operating, create thread
    
    return "left = %s, move = %s, duration = %s"%(left, move, duration)

@app.route("/go")
def go():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    for leftRight in range(2):
        for idx in range(3):
            GPIO.setup(pinList[leftRight][idx], GPIO.OUT)
            GPIO.output(pinList[leftRight][idx], forwardOutput[idx])    
    return "go"

@app.route("/stop")
def stop():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    for leftRight in range(2):
        for idx in range(3):
            GPIO.setup(pinList[leftRight][idx], GPIO.OUT)
            GPIO.output(pinList[leftRight][idx], stopOutput[idx])    
    return "stop"


