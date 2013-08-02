#!/usr/bin/python2.7

from flask import Flask, render_template, g
import source.pandora
import Queue
import threading as thread
import signal
import sys
import json

app = Flask(__name__)

pianobarThread = None
airplayThread = None
cmd_q = Queue.Queue()       #Queue for controlling threads
status_q = Queue.Queue()    #Queue for receiving status from threads

@app.route("/")
def index(name=None):
    return render_template('index.html')

@app.route("/pandora")
def pandora(name=None):
    global pianobarThread
    
    #Check if we need to start the thread
    if pianobarThread is None:
        pianobarThread = source.pandora.pianobar(cmd_q, status_q)
        
    return render_template('pandora.html')
    
@app.route("/airplay")
def airplay(name=None):
    return "Airplay!"
    
@app.route("/status")
def status(name=None):
    try:
        command = status_q.get_nowait()
        print command
        return json.dumps(str(command))
    except Queue.Empty:
        pass
    return "None"


def signal_handler(signal, frame):
    print "Exiting..."
    
    if pianobarThread is None:
        pianobarThread.join()
    
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    #app.debug = True
    app.run('0.0.0.0')