import socketio
import eventlet

# Create a Socket.IO server with debugging enabled
sio = socketio.Server(cors_allowed_origins='*', logger=True)
app = socketio.WSGIApp(sio)

# Define event handlers for the default namespace
@sio.event
def connect(sid, environ):
    print('Client connected to default namespace:', sid)
    print('Headers:', environ)

@sio.event
def disconnect(sid):
    print('Client disconnected from default namespace:', sid)

@sio.event
def message(sid, data):
    print('Message received in default namespace:', data)
    sio.emit('response', {'data': 'Server received your message in default namespace'}, room=sid)

# Define event handlers for the "room" namespace
@sio.on('connect', namespace='/room')
def room_connect(sid, environ):
    print('Client connected to "room" namespace:', sid)
    print('Headers:', environ)

@sio.on('disconnect', namespace='/room')
def room_disconnect(sid):
    print('Client disconnected from "room" namespace:', sid)

@sio.on('message', namespace='/room')
def room_message(sid, data):
    print('Message received in "room" namespace:', data)
    sio.emit('response', {'data': 'Server received your message in "room" namespace'}, room=sid, namespace='/room')

# Wildcard event handler for all namespaces
@sio.event
def any_event(sid, data):
    print('Received event from client:', data)

# Run the server
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
    # eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
