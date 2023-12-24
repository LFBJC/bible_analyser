# from sklearn.feature_extraction.text import TfidfVectorizer
# from scipy.sparse.linalg import svds
from gensim.models import Word2Vec
import numpy as np
import os
from tqdm import tqdm
import pandas as pd
# from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
import re
passage_to_be_compared = '1jo1:7'
include_book = False
book = re.sub('[0-9]+(\\:[0-9]+)?(\\-[0-9]+)?$', '', passage_to_be_compared)
print(book)
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
full_text = []
verse_texts = {}
for path in tqdm(os.listdir('by_verse')):
	# print(re.sub('[0-9]+_[0-9]+\\.txt', '', path))
	f = open('by_verse\\'+path, 'r', encoding='utf-8')
	verse_texts[path] = f.read()
	full_text.append(verse_texts[path])
	f.close()
print('Calculating number of verses by chapter...')
verses_by_chapter = {
	verse_txt.split('_')[0]: max([int(v.split('_')[1].replace('.txt', '')) for v in verse_texts.keys() if v.startswith(verse_txt.split('_')[0])])
	for verse_txt in tqdm(verse_texts.keys())
}
# create the transform
# create the transform
# vectorizer = TfidfVectorizer()
# tokenize and build vocab
# vectorizer.fit(full_text)
# mat2 = vectorizer.transform([v for v in verse_texts.values()])
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
# dim_reducer = TruncatedSVD(n_components=100)
#verse_dots = normalize(dim_reducer.transform(mat2.toarray()))pytho
# verse_dots = dim_reducer.fit_transform(mat2.toarray())
# verse_dots = svds(mat2, k=100)[0]
print('instantiating model...')
model = Word2Vec(full_text, vector_size=100, window=5, min_count=1, sg=0)
print('creating verse dots...')
verse_dots = [np.mean([model.wv[w] for w in v], axis=0) for v in tqdm(verse_texts.values())]
verse_dots_df = pd.DataFrame.from_records(verse_dots).to_csv('verse_dots.csv', index=False)

def verses_in_passage(passage):
	ret = []
	if '-' in passage:
		passage_beginning, passage_end = passage.split('-')[0], passage.split('-')[1]
		initial_chapter = passage_beginning.replace(book, '').split(':')[0]
		initial_verse = passage_beginning.replace(book + initial_chapter + ':', '')
		if ':' in passage_end:
			ending_chapter, ending_verse = passage_end.split(':')[0], passage_end.split(':')[1]
			if ending_chapter != initial_chapter:
				ret = [book + initial_chapter + '_' + str(verse) + '.txt' for verse in range(int(initial_verse), verses_by_chapter[book + initial_chapter])]
				ret += [book + ending_chapter + '_' + str(verse) + '.txt' for verse in range(1, int(ending_verse))]
			else:
				ending_verse = passage_end
				ret = [book + initial_chapter + '_' + str(verse) + '.txt' for verse in range(int(initial_verse), int(ending_verse))]
		else:
			ending_verse = passage_end
			ret = [book + initial_chapter + '_' + str(verse) + '.txt' for verse in range(int(initial_verse), int(ending_verse))]
	else:
		ret = [passage.replace(':', '_') + '.txt']
	return ret


print('creating a passage dot...')
verses_to_be_compared = verses_in_passage(passage_to_be_compared)
verse_dots_passage = list(map(lambda x: list(verse_texts.keys()).index(x), verses_to_be_compared))
passage_dot = np.mean([verse_dots[x] for x in verse_dots_passage], axis=0)
print("Calculating close verses...")
verses_to_consider = sorted(
	range(len(verse_dots)),
	key=lambda x: min([np.linalg.norm(np.array(verse_dots[x]) - np.array(verse_dots[v])) for v in verse_dots_passage]) if x not in verse_dots_passage and ((not include_book and (not list(verse_texts.keys())[x].startswith(book))) or include_book) else 3*len(verse_dots)
)[:10]
print("Plotting...")
plt.clf()
plt.plot(passage_dot[0], passage_dot[1], color='red', marker='^')
book_abbreviation = re.sub('[0-9]+:[0-9]+(-([0-9]+:)?[0-9]+)?', '', passage_to_be_compared)
book = name_by_abbreviation[book_abbreviation]
plt.text(passage_dot[0], passage_dot[1], passage_to_be_compared.replace(book_abbreviation, book))
for dot_i in tqdm(range(len(verse_dots))):
	if dot_i in verses_to_consider:
		verse_doc_name = list(verse_texts.keys())[dot_i]
		verse_book = re.sub('[0-9]+_[0-9]+\.txt', '', verse_doc_name)
		print(verse_doc_name)
		plt.plot(verse_dots[dot_i][0],verse_dots[dot_i][1], color=colors[verse_book], marker='o')
		plt.text(verse_dots[dot_i][0],verse_dots[dot_i][1],name_by_abbreviation[verse_book] + ' ' +(list(verse_texts.keys())[dot_i][2:].replace('_',':').replace('.txt','')))
ax = plt.gca()
# recompute the ax.dataLim
ax.relim()
# update ax.viewLim using the new dataLim
ax.autoscale_view()
plt.show()
