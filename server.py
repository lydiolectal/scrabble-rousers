from flask import Flask, jsonify, render_template, redirect
from src.game import Game

app = Flask(__name__)
game = Game()

# @app.route('/')
# def root():
#     return app.send_static_file('index.html')

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
        tiles = game.cur_player.tiles, score = game.cur_player.recent_score)

@app.route('/', methods = ["POST"])
def next_move():
    game.play_one_move()
    # redirect sends back a response code 302 ("I'm sending you to another location")
    # one of the headers has "location: /" -- the browser then knows to follow
    # it by sending a GET request to that URL.
    return redirect("/")
