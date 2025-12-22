#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from composerstop100 import get_specifics, game_one_turn
from unidecode import unidecode
from datetime import datetime

app = Flask(__name__, template_folder='templates')


date = datetime.now()
idx = (datetime(date.year, date.month, date.day).timetuple().tm_yday)%100
first_name, last_name, summary, gap_text, summary_token_set, summary_token_ascii, link, title = get_specifics(idx)
finished_bool = False
words_used = list()
tries = list()
title_progress = [i for i in title.split()]
title_blank = ['_'*len(i) for i in title.split()]


@app.route('/', methods=('GET',))
@app.route('/index')
def index():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        return None


@app.route('/game', methods=['GET',"POST"])
def game(title_blank=title_blank, title=title, gap_text=gap_text, words_used=words_used, summary=summary, link=link):


    if request.method == 'GET':

        game_text = ' '.join([i[0] for i in gap_text])
        return render_template('game.html', title=" ".join(title_blank), game_text=game_text, words_used=words_used)

    elif request.method == 'POST':

        guess = request.form.get("guess")
        gap_text, words_used, finished_bool = game_one_turn(first_name, last_name, gap_text, summary_token_set, summary_token_ascii, guess, words_used)
        game_text = ' '.join([i[0] for i in gap_text])

        tries.append(guess)

        if finished_bool == True:
            return render_template('correct.html', title=title, summary=summary, words_used=words_used, tries=len(set(tries)), link=link)

        if guess in [t.lower() for t in title_progress] or guess in [unidecode(t.lower()) for t in title_progress] :
            title_blank = list()
            for i in title_progress:
                if i.lower() == guess or (unidecode(i.lower())) == guess:
                    title_blank.append(i)
                else:
                    title_blank.append('_'*len(i))

    return render_template('game.html', title=" ".join(title_blank), game_text=game_text, words_used=words_used)


@app.route('/surrender', methods=['GET',"POST"])
def surrender(title_blank=title_blank, title=title, gap_text=gap_text, words_used=words_used, summary=summary, link=link):
    return render_template('surrender.html', title=title, summary=summary, words_used=words_used, link=link)
        


if __name__ == "__main__":
    app.run()