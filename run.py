# run.py

import os
import time
import tasks
import vars

from flask import session
from flask_socketio import SocketIO, join_room

from app import create_app

from gevent import monkey
monkey.patch_all(subprocess=True)

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
app.config['SECRET_KEY'] = vars.key
socketio = SocketIO(app, message_queue= vars.message_queue)


@socketio.on('connect')
def socket_connect():
    pass


@socketio.on('join_room')
def on_room(json):

    room = str(session['uid'])
    referrer = json['referrer']
    join_room(room)
    print('\t\t\t|-----Room ID: ' + room)
    print('\t\t\t|-----Referrer: ' + referrer)


@socketio.on('request account')
def request_account(json, methods=['GET', 'POST']):
    print (time.strftime("%m-%d-%Y_%H:%M:%S") + '\tQueue request received: ' + str(json))
    room = str(session['uid'])
    print("Room: {}".format(room))
    try:
        tasks.celery_create_account.delay(json['username'], json['fullname'], json['reason'], session=room)
    except Exception as e:
        print(time.strftime("%m-%d-%Y_%H:%M:%S") + "\tError in account creation: ", e)
        socketio.emit("Account creation failed", room)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
