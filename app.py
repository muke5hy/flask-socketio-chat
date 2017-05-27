#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect

import time;

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


class SimpleChat(Namespace):

    def on_chat_event(self, message):
        session['user'] = session.get('user', 'anonymous')
        localtime = time.localtime(time.time())
        emit('response',
             {'msg': message['data'], 'user': session['user'], 'time': localtime},
             broadcast=True)

socketio.on_namespace(SimpleChat('/chat'))


if __name__ == '__main__':
    socketio.run(app, debug=True)
