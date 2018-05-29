from flask import Flask, jsonify, render_template, redirect
from src.game import Game

app = Flask(__name__)
game = Game()

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

@app.route('/', methods = ["GET"])
def root():
    # TODO: law of Demeter (bug Jordan)
    return render_template("index.html", board = game.board.tiles,
        player = game.cur_player.name, tiles = " ".join(game.cur_player.tiles),
        score = game.cur_player.recent_score)

@app.route('/', methods = ["POST"])
def next_move():
    successful_play = game.play_one_move()
    if successful_play:
        return redirect("/")
    else:
        return redirect("/end")

@app.route('/end', methods = ["GET"])
def end():
    return render_template("end.html")
