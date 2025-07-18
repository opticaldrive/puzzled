from flask import Flask, render_template
from flask_socketio import SocketIO, emit
    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')  # Changed from my_event to message
def handle_message(message):
    print('Received message:', message)
    emit('message', message)  # Changed to emit 'message' event with the message itself

if __name__ == '__main__':
    socketio.run(app)