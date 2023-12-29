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
passage_to_be_compared = '1co1:1-16:24'
max_passages = 100
book = re.sub('[0-9]+(\\:[0-9]+)?(\\-[0-9]+(\\:[0-9]+)?)?$', '', passage_to_be_compared)
excluded_books = ['1jo']
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
if ':' not in passage_to_be_compared:
	passage_chapters = [1]
	if '-' in passage_to_be_compared:
		last_verse = int(passage_to_be_compared.split('-')[1])
	else:
		last_verse = int(passage_to_be_compared.replace(book, ''))
elif passage_to_be_compared.count(':') > 1:
	begin_end_passage = passage_to_be_compared.split('-')
	begin_chapter = int(begin_end_passage[0].replace(book, '').split(':')[0])
	end_chapter = int(begin_end_passage[1].replace(book, '').split(':')[0])
	passage_chapters = range(begin_chapter, end_chapter+1)
	last_verse = int(passage_to_be_compared.split('-')[1].split(':')[1])
else:
	passage_chapters = [int(passage_to_be_compared.split(':')[0].replace(book, ''))]
	if '-' in passage_to_be_compared:
		last_verse = int(passage_to_be_compared.split(':')[1].split('-')[1])
	else:
		last_verse = int(passage_to_be_compared.split(':')[1])
verses_by_chapter = pd.read_csv("Verses by chapter.csv")
verse_dots_df = pd.read_csv('verse_dots.csv')

print('creating a passage dot...')
same_book = (verse_dots_df['Book'] == book)
chapter_in_passage = verse_dots_df['Chapter'].map(lambda ch: ch in passage_chapters)
verse_in_passage = np.logical_and(chapter_in_passage, verse_dots_df[['Chapter', "Verse"]].apply(lambda row: row['Chapter'] != max(passage_chapters) or row['Verse'] <= last_verse, axis=1))
verse_dots_passage = verse_dots_df[np.logical_and(np.logical_and(same_book, chapter_in_passage), verse_in_passage)]
passage_dot = verse_dots_passage[[c for c in verse_dots_passage.columns if c not in ['Book', 'Chapter', 'Verse']]].mean()
verse_dots_df = verse_dots_df[~np.logical_and(np.logical_and(same_book, chapter_in_passage), verse_in_passage)]
verse_dots_df = verse_dots_df[~verse_dots_df['Book'].isin(excluded_books)]
print("Calculating close verses...")
verse_dots_df['distance'] = verse_dots_df[[c for c in verse_dots_passage.columns if c not in ['Book', 'Chapter', 'Verse']]].apply(lambda x: np.linalg.norm(x - passage_dot))
verse_dots_df = verse_dots_df.sort_values(by='distance')
def verse_in_passage_function(verse, passage):
	return np.logical_and(
		verse['Book'] == passage['Book'],
		np.logical_and(
			passage['Initial Chapter'] < verse['Chapter'] < passage['Last Chapter'],
			passage['Initial Verse'] < verse['Verse'] < passage['Last Verse']
		)
	)
passages = pd.DataFrame()
i = 0
while i < verse_dots_df.shape[0] and passages.shape[0] < max_passages:
	row = verse_dots_df.iloc[i]
	next_different_passage = next(
		j for j in range(i, verse_dots_df.shape[0])
		if verse_dots_df['Book'].iloc[j] != row['Book'] or verse_dots_df["Chapter"].iloc[j] != row["Chapter"] or\
		(
			(verse_dots_df["Chapter"].iloc[j] == row["Chapter"] + 1) and
			not (verses_by_chapter[
				np.logical_and(verses_by_chapter["Book"] == row["Book"],
							   verses_by_chapter['Chapter'] == row['Chapter'])
			]['Number of verses'].iloc[0] in verse_dots_df.iloc[i:j]['Verse'].values)
		) and not passages.map(lambda x: verse_in_passage_function(verse_dots_df.iloc[j], x)).any()
	)
	passages = pd.concat([
		passages, pd.DataFrame([{
			'Book': row['Book'],
			'Initial_Chapter': min(verse_dots_df['Chapter'].iloc[i:next_different_passage]),
			'Initial_Verse': min(verse_dots_df['Verse'].iloc[i:next_different_passage]),
			"Last_Chapter": max(verse_dots_df['Chapter'].iloc[i:next_different_passage]),
			'Last_Verse': max(verse_dots_df['Verse'].iloc[i:next_different_passage]),
			**{c: verse_dots_df[c].iloc[i:next_different_passage].mean() for c in verse_dots_passage.columns if c not in ['Book', 'Chapter', 'Verse', 'distance']}
		}])
	], ignore_index=True)
	remove = []
	for j in passages.index:
		if j not in remove:
			pass_j = passages.iloc[j]
			for k in passages.index:
				if k not in remove and passages.loc[k, 'Book'] == passages.loc[j, 'Book']:
					if passages['Initial_Chapter'].loc[k] == pass_j['Last_Chapter'] + 1:
						if pass_j['Last_Verse'] == verses_by_chapter[
								np.logical_and(verses_by_chapter["Book"] == pass_j["Book"],
											   verses_by_chapter['Chapter'] == pass_j['Last_Chapter'])
							]['Number of verses'].iloc[0]:
							passages.at[j, 'Last_Chapter'] = passages.loc[k]['Last_Chapter']
							passages.at[j, 'Last_Verse'] = passages.iloc[k]['Last_Verse']
							remove.append(k)
							break
					elif passages['Last_Chapter'].loc[k] == pass_j['Initial_Chapter'] - 1:
						if passages['Last_Verse'].loc[k] == verses_by_chapter[
							np.logical_and(verses_by_chapter["Book"] == pass_j["Book"],
										   verses_by_chapter['Chapter'] == pass_j['Initial_Chapter'])
						]['Number of verses'].iloc[0]:
							passages.at[j, 'Initial_Chapter'] = passages.loc[k]['Initial_Chapter']
							passages.at[j, 'Initial_Verse'] = passages.loc[k]['Initial_Verse']
							remove.append(k)
							break
	passages = passages.drop(index=remove)
	i = next_different_passage
del verse_dots_df
print("Plotting...")
plt.clf()
plt.plot(passage_dot[0], passage_dot[1], color='red', marker='^')
book_abbreviation = book
book = name_by_abbreviation[book]
plt.text(passage_dot[0], passage_dot[1], passage_to_be_compared.replace(book_abbreviation, book))
for i, row in tqdm(passages.iterrows()):
	verse_book = row['Book']
	if row['Initial_Chapter'] == row['Last_Chapter']:
		if row['Initial_Verse'] == row['Last_Verse']:
			passage_string = str(row['Initial_Chapter']) + ':' + str(row['Initial_Verse'])
		else:
			passage_string = str(row['Initial_Chapter']) + ':' + str(row['Initial_Verse']) + '-' + str(row["Last_Verse"])
	else:
		passage_string = str(row['Initial_Chapter']) + ':' + str(row['Initial_Verse']) + '-' + str(row['Last_Chapter']) + ':' + str(row["Last_Verse"])
	vector = row[[c for c in passages.columns if c not in ['Book', "Initial_Chapter", "Initial_Verse", "Last_Chapter", "Last_Verse", 'distance']]]
	plt.plot(vector[0],vector[1], color=colors[verse_book], marker='o')
	plt.text(vector[0],vector[1], f'{name_by_abbreviation[verse_book]} {passage_string}')
ax = plt.gca()
# recompute the ax.dataLim
ax.relim()
# update ax.viewLim using the new dataLim
ax.autoscale_view()
plt.show()
