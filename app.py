from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room
import logging
from utils.whiteboard_utils import create_whiteboard, get_whiteboard, clear_whiteboard, add_drawing_to_whiteboard

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16) 


# Explicitly configure CORS and WebSocket
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Store drawing histories per whiteboard
drawing_histories = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_whiteboard', methods=['POST'])
def new_whiteboard():
    # Get the whiteboard name from the form
    whiteboard_name = request.form.get('whiteboard_name')
    
    if not whiteboard_name:
        return "Whiteboard name is required", 400
    
    # Print the form data (for demonstration)
    print(f"Whiteboard Name Submitted: {whiteboard_name}")
    
    # Create whiteboard and redirect to its page
    whiteboard_id = create_whiteboard(whiteboard_name)
    return redirect(url_for('whiteboard', id=whiteboard_id))

@app.route('/whiteboard/<id>')
def whiteboard(id):
    whiteboard_data = get_whiteboard(id)
    
    if whiteboard_data is not None:
        whiteboard_name = whiteboard_data["name"]
        print("Opening whiteboard: Name:", whiteboard_name, "ID:", id)
        return render_template('whiteboard.html', 
                            whiteboard_id=id, 
                            whiteboard_name=whiteboard_name)
    else:
        return "Whiteboard not found", 404

@socketio.on('join')
def on_join(data):
    print("JOIN REQUEST RECEIVED")
    whiteboard_id = data['whiteboard_id']
    join_room(whiteboard_id)
    
    whiteboard_data = get_whiteboard(whiteboard_id)  # Corrected parameter
    
    # Send existing drawing history for this whiteboard
  
    print("INIT SEND RETRIEVED DRAWING DATA")
    for drawing in whiteboard_data["contents"]:
        # wonky formatting bc idk what on earth i did in the js but this works i think
        emit('draw', {
            'w': whiteboard_id,  # whiteboard ID
            'x0': drawing.get('x0', 0),
            'y0': drawing.get('y0', 0),
            'x1': drawing.get('x1', 0),
            'y1': drawing.get('y1', 0),
            'c': drawing.get('c', '#000000'),  # color
            'l': drawing.get('l', 2)  # line width
        }, room=whiteboard_id)

@socketio.on('draw')
def handle_draw(data):
    whiteboard_id = data['whiteboard_id']
    
    # Initialize history for this whiteboard if not exists
    if whiteboard_id not in drawing_histories:
        drawing_histories[whiteboard_id] = []
    
    # Add drawing to history and broadcast
    drawing_histories[whiteboard_id].append(data)
    emit('draw', data, room=whiteboard_id)
    
    # Optionally save to file
    add_drawing_to_whiteboard(whiteboard_id, data)

@socketio.on('clear_canvas')
def handle_clear(data):
    whiteboard_id = data['whiteboard_id']
    
    # Clear drawing history for this whiteboard
    if whiteboard_id in drawing_histories:
        drawing_histories[whiteboard_id].clear()
    
    # Clear the whiteboard in storage
    clear_whiteboard(whiteboard_id)
    
    # Broadcast clear signal
    emit('clear_canvas', data, room=whiteboard_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, allow_unsafe_werkzeug=True )
