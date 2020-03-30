from celery import Celery
import time
from flask_socketio import SocketIO
import subprocess
import vars

from gevent import monkey
monkey.patch_all(subprocess=True)

broker_url = vars.broker_url
celery = Celery('flask_user_reg', broker=broker_url)

socketio = SocketIO(message_queue=vars.message_queue)


def send_msg(event, room):
   print("Post '{}' to room '{}'".format(event,room))
   socketio.emit(event, room=room)


@celery.task
def celery_create_account(username, fullname, reason, session):
    room = session
    print(time.strftime("%m-%d-%Y_%H:%M:%S") + '\tUser ' + username + ' added to queue')
    send_msg('creating account', room)
    print(username)
    subprocess.call(["/opt/rabbitmq_agents/flask_producer.py", "ohpc_account_create", username])
    print(time.strftime("%m-%d-%Y_%H:%M:%S") + '\tAccount successfully created for ' + username)
    send_msg('account ready', room)
