from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room
import logging
import secrets
import time
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16) 

# log the stuff yay
logging.basicConfig(level=logging.DEBUG)

# configure websockets and uh cors stuff
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# we store chat rooms in here and the messages are inside this
chat_rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_chatroom', methods=['POST'])
def new_chatroom():
    # the person sends the chatroomname
    chatroom_name = request.form.get('chatroom_name')
    
    if not chatroom_name:
        return "You need to put a chatroom name in!", 400
    
    # make UUIDs for chatroom names i kept forgetting this lol
    chatroom_id = str(uuid.uuid4())
    
    chat_rooms[chatroom_id] = {
        'name': chatroom_name,
        'messages': []
    }
    
    return redirect(url_for('chatroom', id=chatroom_id))

@app.route('/chatroom/<id>')
def chatroom(id):
    if id not in chat_rooms:
        return "Chatroom not found :( ", 404
    
    chatroom_name = chat_rooms[id]['name']
    return render_template('chatroom.html', 
                           chatroom_id=id, 
                           chatroom_name=chatroom_name)

@socketio.on('join')
def on_join(data):
    chatroom_id = data['chatroom_id']
    username = data.get('username', 'Anonymous')
    

    join_room(chatroom_id)
    
    if chatroom_id in chat_rooms:
        for message in chat_rooms[chatroom_id]['messages']:
            emit('receive_message', message, room=chatroom_id)

@socketio.on('send_message')
def handle_message(data):
    chatroom_id = data['chatroom_id']
    message = data['message']
    username = data.get('username', 'Anonymous')
    
    message_data = {
        'username': username,
        'message': message,
        'timestamp': int(time.time())
    }
    
    if chatroom_id in chat_rooms:
        chat_rooms[chatroom_id]['messages'].append(message_data)
    
    emit('receive_message', message_data, room=chatroom_id)

@socketio.on('clear_chat')
def handle_clear(data):
    chatroom_id = data['chatroom_id']
    
    if chatroom_id in chat_rooms:
        chat_rooms[chatroom_id]['messages'].clear()
    
    emit('clear_chat', room=chatroom_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5002, allow_unsafe_werkzeug=True)
