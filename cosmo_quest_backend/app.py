from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

players_data = []

@app.route('/')
def index():
    return 'Cosmo Quest Server Running!'

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('questCompleted')
def handle_quest(data):
    print(f"Quest completed by {data['player']}: {data['questId']}")
    found = next((p for p in players_data if p['player'] == data['player']), None)
    if found:
        found['level'] = data['level']
    else:
        players_data.append({'player': data['player'], 'level': data['level']})

    emit('updateLeaderboard', players_data, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
