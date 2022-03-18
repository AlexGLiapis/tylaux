from flask import Flask, render_template, request, redirect, url_for, jsonify, escape
from flask_bootstrap import Bootstrap
from models import app, db, Word
from tools import GameState
import random
import os
import sys

bootstrap = Bootstrap(app)
game = GameState()

@app.route('/', methods=['GET', 'POST'])
def index():
    debug_text=""
    if request.method == 'GET':
        return render_template('index.html', result=None, guesses=None, debug_text=debug_text)
    else:
        # TODO: Freeze on getting correct answer or running out of turns.
        if request.form['Input'] is not None:
            result = game.set_guess(request.form['Input'])
            debug_text = game.answer + ", " + str(game.curr_turn) + ", " + str(game.guess_hist)
            return render_template('index.html', result=result, guesses=game.guess_hist, debug_text=debug_text)

#def guess():
#    return 0
#@app.route('/custom/', methods=['GET', 'POST'])
#def set_custom():
#    return 0


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4567)
    app.run()
