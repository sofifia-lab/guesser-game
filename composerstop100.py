#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import wikipedia

import string
import random

import os
import spacy
nlp = spacy.load('en_core_web_sm')

from unidecode import unidecode

from bs4 import BeautifulSoup



stop_words = [i.strip() for i in open('stopwords.txt', 'r', encoding='utf-8').readlines()]
punctuation = [i for i in string.punctuation]


# list taken from the source code of: https://classicalmusiconly.com/lists/top/composers
top100composers = {"follows": [{"last_name": "Beethoven", "slug": "ludwig-van-beethoven", "first_name": "Ludwig van", "follows": 10302, "has_pic": True}, {"last_name": "Mozart", "slug": "wolfgang-amadeus-mozart", "first_name": "Wolfgang Amadeus", "follows": 9916, "has_pic": True}, {"last_name": "Bach", "slug": "johann-sebastian-bach", "first_name": "Johann Sebastian", "follows": 9609, "has_pic": True}, {"last_name": "Tchaikovsky", "slug": "pyotr-ilyich-tchaikovsky", "first_name": "Pyotr Ilyich", "follows": 8126, "has_pic": True}, {"last_name": "Chopin", "slug": "frederic-chopin", "first_name": "Fr\u00e9d\u00e9ric", "follows": 7036, "has_pic": True}, {"last_name": "Brahms", "slug": "johannes-brahms", "first_name": "Johannes", "follows": 5899, "has_pic": True}, {"last_name": "Vivaldi", "slug": "antonio-vivaldi", "first_name": "Antonio", "follows": 5693, "has_pic": True}, {"last_name": "Schubert", "slug": "franz-schubert", "first_name": "Franz", "follows": 5385, "has_pic": True}, {"last_name": "Debussy", "slug": "claude-debussy", "first_name": "Claude", "follows": 4721, "has_pic": True}, {"last_name": "Handel", "slug": "george-frideric-handel", "first_name": "George Frideric", "follows": 4638, "has_pic": True}, {"last_name": "Rachmaninoff", "slug": "sergei-rachmaninoff", "first_name": "Sergei", "follows": 4630, "has_pic": True}, {"last_name": "Wagner", "slug": "richard-wagner", "first_name": "Richard", "follows": 3919, "has_pic": True}, {"last_name": "Dvo\u0159\u00e1k", "slug": "antonin-dvorak", "first_name": "Anton\u00edn", "follows": 3817, "has_pic": True}, {"last_name": "Mendelssohn", "slug": "felix-mendelssohn", "first_name": "Felix", "follows": 3735, "has_pic": True}, {"last_name": "Verdi", "slug": "giuseppe-verdi", "first_name": "Giuseppe", "follows": 3547, "has_pic": True}, {"last_name": "Liszt", "slug": "franz-liszt", "first_name": "Franz", "follows": 3535, "has_pic": True}, {"last_name": "Shostakovich", "slug": "dmitri-shostakovich", "first_name": "Dmitri", "follows": 3270, "has_pic": True}, {"last_name": "Haydn", "slug": "joseph-haydn", "first_name": "Joseph", "follows": 3209, "has_pic": True}, {"last_name": "Stravinsky", "slug": "igor-stravinsky", "first_name": "Igor", "follows": 3188, "has_pic": True}, {"last_name": "Mahler", "slug": "gustav-mahler", "first_name": "Gustav", "follows": 3118, "has_pic": True}, {"last_name": "Strauss", "slug": "richard-strauss", "first_name": "Richard", "follows": 2947, "has_pic": True}, {"last_name": "Schumann", "slug": "robert-schumann", "first_name": "Robert", "follows": 2819, "has_pic": True}, {"last_name": "Ravel", "slug": "maurice-ravel", "first_name": "Maurice", "follows": 2687, "has_pic": True}, {"last_name": "Puccini", "slug": "giacomo-puccini", "first_name": "Giacomo", "follows": 2354, "has_pic": True}, {"last_name": "Grieg", "slug": "edvard-grieg", "first_name": "Edvard", "follows": 2340, "has_pic": True}, {"last_name": "Sibelius", "slug": "jean-sibelius", "first_name": "Jean", "follows": 2335, "has_pic": True}, {"last_name": "Prokofiev", "slug": "sergei-prokofiev", "first_name": "Sergei", "follows": 2179, "has_pic": True}, {"last_name": "Saint-Sa\u00ebns", "slug": "camille-saint-saens", "first_name": "Camille", "follows": 2173, "has_pic": True}, {"last_name": "Rossini", "slug": "gioachino-rossini", "first_name": "Gioachino", "follows": 2010, "has_pic": True}, {"last_name": "Bart\u00f3k", "slug": "bela-bartok", "first_name": "B\u00e9la", "follows": 1945, "has_pic": True}, {"last_name": "Strauss II", "slug": "johann-strauss-ii", "first_name": "Johann", "follows": 1834, "has_pic": True}, {"last_name": "Rimsky-Korsakov", "slug": "nikolai-rimsky-korsakov", "first_name": "Nikolai", "follows": 1827, "has_pic": True}, {"last_name": "Satie", "slug": "erik-satie", "first_name": "Erik", "follows": 1720, "has_pic": True}, {"last_name": "Monteverdi", "slug": "claudio-monteverdi", "first_name": "Claudio", "follows": 1655, "has_pic": True}, {"last_name": "Faur\u00e9", "slug": "gabriel-faure", "first_name": "Gabriel", "follows": 1652, "has_pic": True}, {"last_name": "Elgar", "slug": "edward-elgar", "first_name": "Edward", "follows": 1551, "has_pic": True}, {"last_name": "Berlioz", "slug": "hector-berlioz", "first_name": "Hector", "follows": 1469, "has_pic": True}, {"last_name": "Schoenberg", "slug": "arnold-schoenberg", "first_name": "Arnold", "follows": 1444, "has_pic": True}, {"last_name": "Mussorgsky", "slug": "modest-mussorgsky", "first_name": "Modest", "follows": 1407, "has_pic": True}, {"last_name": "Bizet", "slug": "georges-bizet", "first_name": "Georges", "follows": 1388, "has_pic": True}, {"last_name": "Gershwin", "slug": "george-gershwin", "first_name": "George", "follows": 1385, "has_pic": True}, {"last_name": "Pachelbel", "slug": "johann-pachelbel", "first_name": "Johann", "follows": 1352, "has_pic": True}, {"last_name": "Purcell", "slug": "henry-purcell", "first_name": "Henry", "follows": 1257, "has_pic": True}, {"last_name": "Scarlatti", "slug": "domenico-scarlatti", "first_name": "Domenico", "follows": 1216, "has_pic": True}, {"last_name": "Offenbach", "slug": "jacques-offenbach", "first_name": "Jacques", "follows": 1161, "has_pic": True}, {"last_name": "Bach", "slug": "carl-philipp-emanuel-bach", "first_name": "Carl Philipp Emanuel", "follows": 1159, "has_pic": True}, {"last_name": "Weber", "slug": "carl-maria-von-weber", "first_name": "Carl Maria von", "follows": 1155, "has_pic": True}, {"last_name": "Smetana", "slug": "bedrich-smetana", "first_name": "Bed\u0159ich", "follows": 1148, "has_pic": True}, {"last_name": "Bruckner", "slug": "anton-bruckner", "first_name": "Anton", "follows": 1145, "has_pic": True}, {"last_name": "Albinoni", "slug": "tomaso-albinoni", "first_name": "Tomaso", "follows": 1141, "has_pic": True}, {"last_name": "Holst", "slug": "gustav-holst", "first_name": "Gustav", "follows": 1114, "has_pic": True}, {"last_name": "Williams", "slug": "ralph-vaughan-williams", "first_name": "Ralph Vaughan", "follows": 1098, "has_pic": True}, {"last_name": "Borodin", "slug": "alexander-borodin", "first_name": "Alexander", "follows": 1048, "has_pic": True}, {"last_name": "Corelli", "slug": "arcangelo-corelli", "first_name": "Arcangelo", "follows": 1032, "has_pic": True}, {"last_name": "Palestrina", "slug": "giovanni-pierluigi-da-palestrina", "first_name": "Giovanni Pierluigi da", "follows": 1023, "has_pic": True}, {"last_name": "Telemann", "slug": "georg-philipp-telemann", "first_name": "Georg Philipp", "follows": 1010, "has_pic": True}, {"last_name": "Copland", "slug": "aaron-copland", "first_name": "Aaron", "follows": 901, "has_pic": True}, {"last_name": "Boccherini", "slug": "luigi-boccherini", "first_name": "Luigi", "follows": 898, "has_pic": True}, {"last_name": "Barber", "slug": "samuel-barber", "first_name": "Samuel", "follows": 894, "has_pic": True}, {"last_name": "Paganini", "slug": "niccolo-paganini", "first_name": "Niccol\u00f2", "follows": 846, "has_pic": True}, {"last_name": "Franck", "slug": "cesar-franck", "first_name": "C\u00e9sar", "follows": 840, "has_pic": True}, {"last_name": "Gluck", "slug": "christoph-willibald-gluck", "first_name": "Christoph Willibald", "follows": 824, "has_pic": True}, {"last_name": "Britten", "slug": "benjamin-britten", "first_name": "Benjamin", "follows": 823, "has_pic": True}, {"last_name": "Scarlatti", "slug": "alessandro-scarlatti", "first_name": "Alessandro", "follows": 801, "has_pic": True}, {"last_name": "Scriabin", "slug": "alexander-scriabin", "first_name": "Alexander", "follows": 797, "has_pic": True}, {"last_name": "Lully", "slug": "jean-baptiste-lully", "first_name": "Jean-Baptiste", "follows": 794, "has_pic": True}, {"last_name": "Donizetti", "slug": "gaetano-donizetti", "first_name": "Gaetano", "follows": 786, "has_pic": True}, {"last_name": "Bruch", "slug": "max-bruch", "first_name": "Max", "follows": 776, "has_pic": True}, {"last_name": "Rameau", "slug": "jean-philippe-rameau", "first_name": "Jean-Philippe", "follows": 752, "has_pic": True}, {"last_name": "Glinka", "slug": "mikhail-glinka", "first_name": "Mikhail", "follows": 751, "has_pic": True}, {"last_name": "des Prez", "slug": "josquin-des-prez", "first_name": "Josquin", "follows": 747, "has_pic": True}, {"last_name": "Pergolesi", "slug": "giovanni-battista-pergolesi", "first_name": "Giovanni Battista", "follows": 736, "has_pic": True}, {"last_name": "Jan\u00e1\u010dek", "slug": "leos-janacek", "first_name": "Leo\u0161", "follows": 724, "has_pic": True}, {"last_name": "Poulenc", "slug": "francis-poulenc", "first_name": "Francis", "follows": 708, "has_pic": True}, {"last_name": "Du Fay", "slug": "guillaume-dufay", "first_name": "Guillaume", "follows": 693, "has_pic": True}, {"last_name": "Cage", "slug": "john-cage", "first_name": "John", "follows": 650, "has_pic": True}, {"last_name": "Messiaen", "slug": "olivier-messiaen", "first_name": "Olivier", "follows": 648, "has_pic": True}, {"last_name": "Gounod", "slug": "charles-gounod", "first_name": "Charles", "follows": 638, "has_pic": True}, {"last_name": "Bellini", "slug": "vincenzo-bellini", "first_name": "Vincenzo", "follows": 632, "has_pic": True}, {"last_name": "Salieri", "slug": "antonio-salieri", "first_name": "Antonio", "follows": 622, "has_pic": True}, {"last_name": "Bingen", "slug": "hildegard-of-bingen", "first_name": "Hildegard of", "follows": 621, "has_pic": True}, {"last_name": "Byrd", "slug": "william-byrd", "first_name": "William", "follows": 616, "has_pic": True}, {"last_name": "Tallis", "slug": "thomas-tallis", "first_name": "Thomas", "follows": 615, "has_pic": True}, {"last_name": "Massenet", "slug": "jules-massenet", "first_name": "Jules", "follows": 608, "has_pic": True}, {"last_name": "Couperin", "slug": "francois-couperin", "first_name": "Fran\u00e7ois", "follows": 599, "has_pic": True}, {"last_name": "Webern", "slug": "anton-webern", "first_name": "Anton", "follows": 578, "has_pic": True}, {"last_name": "Berg", "slug": "alban-berg", "first_name": "Alban", "follows": 576, "has_pic": True}, {"last_name": "Buxtehude", "slug": "dieterich-buxtehude", "first_name": "Dieterich", "follows": 574, "has_pic": True}, {"last_name": "Torelli", "slug": "giuseppe-torelli", "first_name": "Giuseppe", "follows": 566, "has_pic": True}, {"last_name": "Sch\u00fctz", "slug": "heinrich-schutz", "first_name": "Heinrich", "follows": 563, "has_pic": True}, {"last_name": "Machaut", "slug": "guillaume-de-machaut", "first_name": "Guillaume de", "follows": 549, "has_pic": True}, {"last_name": "Victoria", "slug": "tomas-luis-de-victoria", "first_name": "Tomas Luis de", "follows": 536, "has_pic": True}, {"last_name": "P\u00e9rotin", "slug": "perotin", "first_name": "", "follows": 532, "has_pic": True}, {"last_name": "L\u00e9onin", "slug": "leonin", "first_name": "", "follows": 516, "has_pic": True}, {"last_name": "Gabrieli", "slug": "giovanni-gabrieli", "first_name": "Giovanni", "follows": 508, "has_pic": True}, {"last_name": "Biber", "slug": "heinrich-ignaz-franz-von-biber", "first_name": "Heinrich Ignaz Franz von", "follows": 501, "has_pic": True}, {"last_name": "Khachaturian", "slug": "aram-khachaturian", "first_name": "Aram", "follows": 492, "has_pic": True}, {"last_name": "Ockeghem", "slug": "johannes-ockeghem", "first_name": "Johannes", "follows": 489, "has_pic": True}, {"last_name": "Sullivan", "slug": "arthur-sullivan", "first_name": "Arthur", "follows": 479, "has_pic": True}, {"last_name": "Lassus", "slug": "orlande-de-lassus", "first_name": "Orlande de", "follows": 461, "has_pic": True}], "type_id": "composers"}

top100_stripped = {i: {'last_name': c['last_name'], 'first_name': c['first_name']} for i, c in enumerate(top100composers['follows'])}



def return_summary(first_name:str, last_name:str, format='short'):

	query = f'{first_name} {last_name}'

	w = wikipedia.page(query, auto_suggest=False)
	aim = w.title
	summary = w.summary

	soup = BeautifulSoup(w.html(), 'html.parser')

	img_link = str(soup.find('td',{'class':'infobox-image'}).find('img'))
	img_link = img_link.split(' ')

	for i in img_link:
		if i.startswith('src='):
			link = i[7:-1]



def run_game(first_name:str, last_name:str, format='short'):

	query = f'{first_name} {last_name}'

	w = wikipedia.page(query, auto_suggest=False)
	aim = w.title
	summary = w.content#.summary

	soup = BeautifulSoup(w.html(), 'html.parser')

	try:
		img_link = str(soup.find('td',{'class':'infobox-image'}).find('img'))
		img_link = img_link.split(' ')

		for i in img_link:
			if i.startswith('src='):
				link = i[7:-1]

	except AttributeError:
		img_link = str(soup.find('figure',{'typeof':'mw:File/Thumb'}).find('img'))
		img_link = img_link.split(' ')

		for i in img_link:
			if i.startswith('src='):
				link = i[7:-1]

	print(link)


	summary_tokenized = word_tokenize(summary)
	summary_token_set= set([i.lower() for i in summary_tokenized])
	
	initial = [t if t in stop_words or t in punctuation else "_"*len(t) for t in summary_tokenized]
	print(" ".join(initial))

	gap_text = [i for i in zip(initial, summary_tokenized)]


	words_used = list()

	title = False
	title_full = [i.lower() for i in query.split()]
	title_aim = list()

	while title == False:

		user_word = input('Word: ')
		user_word = user_word.lower()
		user_word = user_word.strip()

		if user_word in summary_token_set and user_word not in words_used:
			
			if user_word in title_full:
				if user_word == last_name.lower():
					title = True
					print('YOU GUESSED IT !!')
					print(summary)
					break

				else:
					title_aim.append(user_word)
					for i, (x, y) in enumerate(gap_text):
						if x == '_'*len(y) and y.lower() == user_word:
							gap_text[i] = (y, y)
						else:
							gap_text[i] = (x, y)

			else:
				for i, (x, y) in enumerate(gap_text):
					if x == '_'*len(y) and y.lower() == user_word:
						gap_text[i] = (y, y)
					else:
						gap_text[i] = (x, y)

			inprogress = " ".join([i[0] for i in gap_text])
			print(inprogress)
			words_used.append(user_word)

		elif user_word.lower() in words_used:
			print('Word already used.')
			continue

		else:
			words_used.append(user_word)

		print(words_used)



def get_specifics(i=None):

	top100_stripped = {i: {'last_name': c['last_name'], 'first_name': c['first_name']} for i, c in enumerate(top100composers['follows'])}

	if i == None:
		i = random.randint(0, 100)

	composer_first = top100_stripped[i]['first_name']
	composer_last = top100_stripped[i]['last_name']

	query = f'{composer_first} {composer_last}'

	w = wikipedia.page(query, auto_suggest=False)
	aim = w.title
	summary = w.summary

	soup = BeautifulSoup(w.html(), 'html.parser')

	try:
		img_link = str(soup.find('td',{'class':'infobox-image'}).find('img'))
		img_link = img_link.split(' ')

		for i in img_link:
			if i.startswith('src='):
				link = i[7:-1]

	except AttributeError:
		img_link = str(soup.find('figure',{'typeof':'mw:File/Thumb'}).find('img'))
		img_link = img_link.split(' ')

		for i in img_link:
			if i.startswith('src='):
				link = i[7:-1]

	summary_tokenized = [token.text for token in nlp(summary)]
	summary_token_ascii = set([unidecode(i.lower()) for i in summary_tokenized])
	summary_token_set= set([i.lower() for i in summary_tokenized])
	
	initial = [t if t in stop_words or t in punctuation else "_"*len(t) for t in summary_tokenized]

	gap_text = [i for i in zip(initial, summary_tokenized)]

	return composer_first, composer_last, summary, gap_text, summary_token_set, summary_token_ascii, link, aim


def game_one_turn(first_name:str, last_name:str, gap_text:list, summary_token_set:set, summary_token_ascii:set, guess:str, words_used:list):


	user_word = guess.lower()
	user_word = user_word.strip()

	if (user_word in summary_token_set or user_word in summary_token_ascii) and (user_word not in words_used):

		if user_word in summary_token_set:
		
			if user_word == last_name.lower():
				return [], [], True

			else:
				for i, (x, y) in enumerate(gap_text):
					if x == '_'*len(y) and y.lower() == user_word:
						gap_text[i] = (y, y)
					else:
						gap_text[i] = (x, y)

			inprogress = " ".join([i[0] for i in gap_text])
			words_used.insert(0, user_word)
			
			return gap_text, words_used, False


		elif user_word in summary_token_ascii:

			if user_word == unidecode(last_name.lower()):
				return [], [], True

			else:
				for i, (x, y) in enumerate(gap_text):
					if x == '_'*len(y) and unidecode(y.lower()) == user_word:
						gap_text[i] = (y, y)
					else:
						gap_text[i] = (x, y)

			inprogress = " ".join([i[0] for i in gap_text])
			words_used.insert(0, user_word)
			
			return gap_text, words_used, False


	elif user_word.lower() in words_used:
		
		return gap_text, words_used, False

	else:
		words_used.insert(0, user_word)

		return gap_text, words_used, False



	return gap_text, words_used, finished_bool


def run():

	first_name, last_name, summary, gap_text, summary_token_set, link, title = get_specifics(4)

	finished_bool = False
	words_used = list()

	print(' '.join([i[0] for i in gap_text]))

	while finished_bool == False:

		guess = input('GUESS: ')
		
		gap_text, words_used, finished_bool = game_one_turn(first_name, last_name, gap_text, summary_token_set, guess, words_used)

		if finished_bool == False:
			print(' '.join([i[0] for i in gap_text]))
			print(words_used)




