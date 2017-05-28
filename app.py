#!/usr/bin/env python
from datetime import datetime
import arrow
from flask import Flask, render_template, session, request, jsonify, redirect
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from utils import auth_required, login_required
from model import Chatter
from model import db

async_mode = 'eventlet'

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None

app.config.from_pyfile('config.py')
db.init_app(app)


@app.route('/')
@login_required
def index():
  return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    session['user'] = request.form.get('username', 'anonymous')
    return redirect(request.args.get("next") or url_for("index"))
  return render_template('login.html')

@app.route('/chat', methods=['GET'])
def chat_history():

  results = db.session.query(Chatter).order_by(Chatter.timestamp.desc()).limit(20)
  data = {'data':[i.serialize for i in results], 'status':'ok'}
  return jsonify(data)

@app.route('/chat/<string:code>/', methods=['DELETE'])
@app.route('/chat/<string:code>/<int:chat_id>', methods=['DELETE'])
@auth_required
def chat_delete(code, chat_id=None):

  if chat_id:
    Chatter.query.filter(Chatter.id == chat_id).delete()
  else:
    Chatter.query.delete()

  db.session.commit()
  data = {'data':[], 'status':'ok'}
  return jsonify(data)



def insert_into_table(obj):
  db.session.add(obj)
  db.session.commit()


class SimpleChat(Namespace):

    def on_chat_event(self, message):
        session['user'] = session.get('user', 'anonymous')
        localtime = arrow.now()

        chat = Chatter(session['user'], message['data'], request.remote_addr, datetime.now())
        insert_into_table(chat)

        emit('response',
             {'message': message['data'], 'username': session['user'], 'timestamp': localtime.humanize(), 'type':'chat'},
             broadcast=True)


    def on_connect_event(self, message):
        session['user'] = session.get('user', 'anonymous')
        localtime = arrow.now().humanize()

        emit('response',
             {'msg': message['data'], 'username': session['user'], 'timestamp': localtime, 'type':'connection'},
             broadcast=True)

    def on_pagination_event(self, message):
        session['user'] = session.get('user', 'anonymous')
        localtime = arrow.now().humanize()
        emit('response',
             {'msg': message['data'], 'username': session['user'], 'timestamp': localtime, 'type':'chat'},
             broadcast=True)

socketio.on_namespace(SimpleChat('/chat'))


if __name__ == '__main__':
    socketio.run(app, debug=True)
