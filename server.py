import socketio
import eventlet

# Create a Socket.IO server with debugging enabled
sio = socketio.Server(cors_allowed_origins='*', logger=True)
app = socketio.WSGIApp(sio)

# Define event handlers
@sio.event
def connect(sid, environ):
    print('Client connected:', sid)
    print('Headers:', environ)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
def message(sid, data):
    print('Message received:', data)
    sio.emit('response', {'data': 'Server received your message'}, room=sid)

@sio.event
def ping(sid):
    print('Received ping from client', sid)
    sio.emit('pong', room=sid)

@sio.event
def pong(sid):
    print('Received pong from client', sid)

# Run the server
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
    # eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
