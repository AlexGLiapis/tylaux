from flask import Flask, render_template, request, redirect, url_for, jsonify, escape
from flask_bootstrap import Bootstrap
import gamestate
import random
import os
import sys

bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home/', methods=['GET', 'POST'])
def index():

@app.route('/guess/<guess_val>', methods='POST')
def guess():

@app.route('/custom/', methods=['GET', 'POST'])
def set_custom():
    


if __name__ == '__main__':
    #app.debug = True
    #app.run(host='0.0.0.0', port=5000)
    app.run()
