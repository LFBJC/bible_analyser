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
verses_by_chapter_df = pd.DataFrame(columns=['Book', 'Chapter', 'Number of verses'])
for verse_txt in tqdm(verse_texts.keys()):
	current_book = re.sub('[0-9]+$', '', verse_txt.split('_')[0])
	current_chapter = re.search('[0-9]+$', verse_txt.split('_')[0]).group()
	if verses_by_chapter_df[np.logical_and(verses_by_chapter_df['Book'] == current_book, verses_by_chapter_df['Chapter'] == current_chapter)].shape[0] > 0:
		verses_by_chapter_df.append({
			'Book': current_book,
			'Chapter': current_chapter,
			'Number of verses': max([int(v.split('_')[1].replace('.txt', '')) for v in verse_texts.keys() if v.startswith(verse_txt.split('_')[0])])
		})
verses_by_chapter_df.to_csv("Verses by chapter.csv")
# create the transform
# create the transform
# vectorizer = TfidfVectorizer()
# tokenize and build vocab
# vectorizer.fit(full_text)
# mat2 = vectorizer.transform([v for v in verse_texts.values()])
# summarize
#print(vectorizer.vocabulary_)
#mat = [v.toarray() for v in list(books_vectors.values())]
# dim_reducer = TruncatedSVD(n_components=100)
#verse_dots = normalize(dim_reducer.transform(mat2.toarray()))pytho
# verse_dots = dim_reducer.fit_transform(mat2.toarray())
# verse_dots = svds(mat2, k=100)[0]
print('instantiating model...')
model = Word2Vec(full_text, vector_size=100, window=5, min_count=1, sg=0)
print('creating verse dots...')
verse_to_dots_records = []
for k, v in tqdm(verse_texts.items()):
	verse_to_dots_records.append({
		'Book': re.sub('[0-9]+$', '', k.split('_')[0]),
		'Chapter': int(re.search('[0-9]+$', k.split('_')[0]).group()),
		'Verse': int(k.split('_')[1].replace('.txt', '')),
		**{i: v for i, v in enumerate(np.mean([model.wv[w] for w in v], axis=0))}
	})
verse_dots_df = pd.DataFrame.from_records(verse_to_dots_records)
verse_dots_df.to_csv('verse_dots.csv', index=False)
