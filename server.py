from flask import Flask, jsonify
from src.game import Game

app = Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/start', methods = ["GET"])
def start_game():
    """
    Initialize game and return JSON needed to render beginning game state.
    """
    game = Game()
    game_state = {
                    "state": game.board.tiles,
                    "player1_tiles": game.player1.tiles,
                    "player2_tiles": game.player2.tiles,
                 }
    return jsonify(game_state)

@app.route('/next-move', methods = ["GET"])
def next_move():
    return 'Hello, World!'
    game = Game()
    # TODO: pass in alternating 1 or 0 for current player.
    game.play_one_move()

@app.route('/end-game', methods = ["GET"])
def end_game():
    return 'Hello, World!'
    game = Game()
    game.play_one_move()
