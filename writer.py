import os
import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from bs4.element import Comment
url = 'https://www.bible.com/pt/bible/';
versions_vt = [(904, 'WLC'), (129, 'NVI'), (212, 'ARC')];
versions_nt = [(183, 'TR1894'), (129, 'NVI'), (212, 'ARC')];
books_vt = ['GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', '1SA', '2SA', '1KI', '2KI', '1CH', '2CH', 'EZR', 'NEH', 'EST', 'JOB', 'PSA', 'PRO', 'ECC', 'SNG', 'ISA', 'JER', 'LAM', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO', 'OBA', 'JON', 'MIC', 'NAM', 'HAB', 'ZEP', 'HAG', 'ZEC', 'MAL']
books_nt = ['MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV'];
chapters_vt = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4]
chapters_nt = [28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22];
def tag_visible(element):
	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True
def get_encoding(soup):
	encod = soup.meta.get('charset');
	if encod == None:
		encod = soup.meta.get('content-type');
		if encod == None:
			encod = soup.meta.get('content');
	return encod
os.mkdir('by_chapter/');
os.mkdir('by_book/')
 for i in range(len(books_vt)):
 	book_string = u'';
 	f1 = open('by_book/'+books_vt[i]+'.txt','w+',encoding='utf-8');
 	for j in range(1,chapters_vt[i]+1):
 		f2 = open('by_chapter/'+books_vt[i]+str(j)+'.txt','w+',encoding='utf-8');
 		str_to_be_written = u'';
 		for v in versions_vt:
 			get_url = url + str(v[0]) + '/' + books_vt[i] + '.' + str(j) + '.' + str(v[1]);
 			req = Request(get_url, headers={'User-Agent': 'Mozilla/71.0'});
 			webpage = urlopen(req).read();
 			print('Funcionou: ', get_url);
 			sopa = BeautifulSoup(webpage, 'html.parser');
 			visible_texts = filter(tag_visible, sopa.findAll(text=True));
 			text = u" ".join(t.strip() for t in visible_texts)
 			str_to_be_written += text;
 			time.sleep(1);
 		f2.write(str_to_be_written);
 		book_string += str_to_be_written;
 		f2.close();
 	f1.write(book_string)
 	f1.close();
for i in range(len(books_nt)):
	book_string = u'';
	f1 = open('by_book/'+books_nt[i]+'.txt','w+',encoding='utf-8');
	for j in range(1,chapters_nt[i]+1):
		f2 = open('by_chapter/'+books_nt[i]+str(j)+'.txt','w+',encoding='utf-8');
		str_to_be_written = u'';
		for v in versions_nt:
			get_url = url + str(v[0]) + '/' + books_nt[i] + '.' + str(j) + '.' + str(v[1]);
			req = Request(get_url, headers={'User-Agent': 'Mozilla/71.0'});
			webpage = urlopen(req).read();
			print('Funcionou: ', get_url);
			sopa = BeautifulSoup(webpage, 'html.parser');
			visible_texts = filter(tag_visible, sopa.findAll(text=True));
			text = u" ".join(t.strip() for t in visible_texts)
			str_to_be_written += text;
			time.sleep(1);
		f2.write(str_to_be_written);
		book_string += str_to_be_written;
		f2.close();
	f1.write(book_string)
	f1.close();