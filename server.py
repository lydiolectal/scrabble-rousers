from flask import Flask, jsonify, render_template, redirect, url_for
from src.game import Game

app = Flask(__name__)
game = Game()
game_over = False

# @app.route('/start', methods = ["GET"])
# def start_game():
#     """
#     Initialize game and return JSON needed to render beginning game state.
#     """
#     game = Game()
#     game_state = {
#                     "state": game.board.tiles,
#                     "player1_tiles": game.player1.tiles,
#                     "player2_tiles": game.player2.tiles,
#                  }
#     return jsonify(game_state)

@app.route('/', methods = ["GET"])
def root():
    # TODO: law of Demeter (bug Jordan)
    if game_over:
        return render_template("end.html")
    else:
        return render_template("index.html", board = game.board.tiles,
            player = game.cur_player.name, tiles = " ".join(game.cur_player.tiles),
            score = game.cur_player.recent_score)

@app.route('/', methods = ["POST"])
def next_move():
    global game_over
    if game_over:
        global game
        game = Game()
        game_over = False
        return redirect("/")
    else:
        successful_play = game.play_one_move()
        if not successful_play:
            game_over = True
        return redirect("/")
