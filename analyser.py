from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os
from sklearn.decomposition import FastICA
import matplotlib.pyplot as plt
import re
def normalize (matrix):
	center = matrix.mean(0)
	distances = np.array([np.linalg.norm(r-center) for r in matrix])
	mean_dist = distances.mean()
	matrix = [(r-center)/mean_dist for r in matrix]
	return matrix
name_by_abbreviation = {
	'gn': 'Genesis','ex': 'Exodo', 'lv': 'Levitico', 'nm': 'Numeros', 'dt':'Deuteronomio',
	'js': 'Josue', 'jz': 'Juizes', 'rt': 'Rute', '1sm': '1 Samuel', '2sm': '2 Samuel',
	'1rs': '1 Reis', '2rs': '2 Reis', '1cr': '1 Cronicas', '2cr': '2 Cronicas', 'ed': 'Esdras',
	'ne': 'Neemias', 'et': 'Ester', 'jó': 'Jó', 'sl': 'Salmos', 'pv': 'Provérbios',
	'ec': 'Eclesiastes','ct': 'Cantares','is': 'Isaias', 'jr': 'Jeremias', 'lm': 'Lamentações',
	'ez': 'Ezequiel', 'dn': 'Daniel','os': 'Oseias', 'jl': 'Joel', 'am': 'Amos', 'ob': 'Obadias',
	'jn': 'Jonas', 'mq': 'Miqueias', 'na': 'Naum', 'hc': 'Habacuque', 'sf': 'Sofonias', 'ag': 'Ageu',
	'zc': 'Zacarias', 'ml': 'Malaquias', 'mt': 'Mateus', 'mc': 'Marcos', 'lc': 'Lucas', 'jo': 'Joao',
	'atos': 'Atos', 'rm': 'Romanos', '1co': '1 Corintios', '2co': '2 Corintios', 'gl': 'Galatas',
	'ef': 'Efesios', 'fp': 'Filipenses', 'cl': 'Colosenses', '1ts': '1 Tessalonisenses',
	'2ts': '2 Tessalonisenses', '1tm': '1 Timoteo', '2tm': '2 Timoteo', 'tt': 'Tito',
	'fm': 'Filemom', 'hb': 'Hebreus', 'tg': 'Tiago', '1pe': '1 Pedro', '2pe': '2 Pedro',
	'1jo': '1 Joao', '2jo': '2 Joao', '3jo': '3 Joao', 'jd': 'Judas', 'ap': 'Apocalipse'
}
books_texts = {}
for path in os.listdir('by_book'):
	f = open('by_book\\'+path, 'r', encoding='utf-8')
	books_texts[path.replace('.txt','')] = f.read()
	f.close()
chapters_texts = {}
for path in os.listdir('by_chapter'):
	f = open('by_chapter\\'+path, 'r', encoding='utf-8')
	chapters_texts[path] = f.read()
	f.close()
# list of text documents (input for vectorizer)
full_text = [v for v in books_texts.values()]
# create the transform
vectorizer = TfidfVectorizer()
# tokenize and build vocab
mat1 = vectorizer.fit_transform(full_text)
mat2 = vectorizer.transform([v for v in chapters_texts.values()])
# summarize
#print(vectorizer.vocabulary_)
colors = {
	'gn': '#FF0000','ex': '#7f4040', 'lv': '#4c2b26', 'nm': '#594643', 'dt':'#401100',
	'js': '#662e1a', 'jz': '#7f5140', 'rt': '#8c7369', '1sm': '#993d00', '2sm': '#4c2a13',
	'1rs': '#593000', '2rs': '#99754d', '1cr': '#734d00', '2cr': '#4c3913', 'ed': '#595243',
	'ne': '#4B0082', 'et': '#998a4d', 'jó': '#4c4a26', 'sl': '#535900', 'pv': '#7d8060',
	'ec': '#FF8C00','ct': '#305900','is': '#384030', 'jr': '#3e592d', 'lm': '#598c46',
	'ez': '#608068', 'dn': '#005924','os': '#009952', 'jl': '#134d32', 'am': '#269982',
	'ob': '#2d5956', 'jn': '#268299', 'mq': '#607980', 'na': '#005580', 'hc': '#2d4a59',
	'sf': '#13324d', 'ag': '#003380', 'zc': '#234d8c', 'ml': '#606c80', 'mt': '#131b4d',
	'mc': '#0000FF', 'lc': '#000040', 'jo': '#332d59', 'atos': '#464359', 'rm': '#290066',
	'1co': '#4d238c', '2co': '#6c468c', 'gl': '#301040', 'ef': '#756080', 'fp': '#7a0099',
	'cl': '#520066', '1ts': '#802079', '2ts': '#660052', '1tm': '#592d50', '2tm': '#40303a',
	'tt': '#992663', 'fm': '#4d1332', 'hb': '#997387', 'tg': '#8c4662', '1pe': '#990029',
	'2pe': '#7f2039', '1jo': '#592d39', '2jo': '#66000e', '3jo': '#4c131b', 'jd': '#806064',
	'ap': '#000000'
}
#mat = [v.toarray() for v in list(books_vectors.values())]
dim_reducer = FastICA(n_components=2)
#books_dots = normalize(dim_reducer.fit_transform(mat1.toarray()))
books_dots = dim_reducer.fit_transform(mat1.toarray())
plt.clf()
for dot_i in range(len(books_dots)):
	plt.plot(books_dots[dot_i][0],books_dots[dot_i][1], color=colors[list(books_texts.keys())[dot_i].lower()], marker='o')
	plt.text(books_dots[dot_i][0],books_dots[dot_i][1],name_by_abbreviation[list(books_texts.keys())[dot_i].lower()])
ax = plt.gca()
# recompute the ax.dataLim
ax.relim()
# update ax.viewLim using the new dataLim
ax.autoscale_view()
plt.show()
#chapters_dots = normalize(dim_reducer.transform(mat2.toarray()))pytho
chapters_dots = dim_reducer.transform(mat2.toarray())
print('ap1 vector:', chapters_dots[list(chapters_texts.keys()).index('ap1.txt')])
plt.clf()
for dot_i in range(len(chapters_dots)):
	chapters_doc_name = list(chapters_texts.keys())[dot_i]
	print(chapters_doc_name)
	plt.plot(chapters_dots[dot_i][0],chapters_dots[dot_i][1], color=colors[chapters_doc_name[0:re.search("\d*.txt",chapters_doc_name).start()].lower()], marker='o')
	plt.text(chapters_dots[dot_i][0],chapters_dots[dot_i][1],name_by_abbreviation[chapters_doc_name[0:re.search("\d*.txt",chapters_doc_name).start()].lower()]+(list(chapters_texts.keys())[dot_i][2:].replace('.txt','')))
ax = plt.gca()
# recompute the ax.dataLim
ax.relim()
# update ax.viewLim using the new dataLim
ax.autoscale_view()
plt.show()
