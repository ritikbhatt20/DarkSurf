from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from cassandra.cluster import Cluster
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def get_data_from_cassandra():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('employee')

    select_query = "SELECT filename, label, categories FROM lol"
    rows = session.execute(select_query)

    data = [(row.filename, row.label, row.categories) for row in rows]
    
    cluster.shutdown()

    return data

@app.route('/')
def index():
    data = get_data_from_cassandra()
    return render_template('index2.html', data=data)

@socketio.on('update_data')
def update_data():
    while True:
        data = get_data_from_cassandra()
        socketio.emit('data_updated', {'data': data})
        time.sleep(5)

@socketio.on('connect')
def handle_connect():
    emit('data_updated', {'data': get_data_from_cassandra()})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/archive/<filename>')
def view_file(filename):
    # Assuming the HTML files are in the 'archive' directory
    return send_from_directory('../archive', filename)

if __name__ == '__main__':
    socketio.start_background_task(update_data)    
    socketio.run(app, debug=True)

