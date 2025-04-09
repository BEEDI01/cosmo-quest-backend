
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

players = {}
quests = {}

@app.route('/')
def index():
    return "Cosmo Quest Backend is Running!"

@socketio.on('connect')
def on_connect():
    print('A user connected')

@socketio.on('player_joined')
def handle_player(data):
    player_id = data['id']
    players[player_id] = data
    print(f"Player joined: {data}")
    emit('update_players', list(players.values()), broadcast=True)

@socketio.on('update_position')
def update_position(data):
    player_id = data['id']
    if player_id in players:
        players[player_id]['x'] = data['x']
        players[player_id]['y'] = data['y']
    emit('update_players', list(players.values()), broadcast=True)

@socketio.on('complete_quest')
def complete_quest(data):
    player_id = data['id']
    quest = data['quest']
    if player_id not in quests:
        quests[player_id] = []
    if quest not in quests[player_id]:
        quests[player_id].append(quest)
    emit('update_quests', quests, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
