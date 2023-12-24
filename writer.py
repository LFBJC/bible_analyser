# -*- coding: utf-8 -*-
import os
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import quote
url = 'https://www.bibliaonline.com.br/'
#os idiomas originais tinham separado muito o antigo e o novo testamento
versions_vt = ['nvi','acf', 'alep']#(904, 'WLC') - hebraico
versions_nt = ['nvi','acf', 'receptus']#(183, 'TR1894') - grego
books_vt = ['gn', 'ex', 'lv', 'nm', 'dt', 'js', 'jz', 'rt', '1sm', '2sm', '1rs', '2rs', '1cr', '2cr', 'ed', 'ne', 'et', 'jó', 'sl', 'pv', 'ec', 'ct', 'is', 'jr', 'lm', 'ez', 'dn', 'os', 'jl', 'am', 'ob', 'jn', 'mq', 'na', 'hc', 'sf', 'ag', 'zc', 'ml']
books_nt = ['mt', 'mc', 'lc', 'jo', 'atos', 'rm', '1co', '2co', 'gl', 'ef', 'fp', 'cl', '1ts', '2ts', '1tm', '2tm', 'tt', 'fm', 'hb', 'tg', '1pe', '2pe', '1jo', '2jo', '3jo', 'jd', 'ap']
chapters_vt = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4]
chapters_nt = [28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22]
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
def get_encoding(soup):
    encod = soup.meta.get('charset')
    if encod == None:
        encod = soup.meta.get('content-type')
        if encod == None:
            encod = soup.meta.get('content')
    return encod
os.makedirs('by_chapter/', exist_ok=True)
os.makedirs('by_book/', exist_ok=True)
os.makedirs('by_verse', exist_ok=True)
'''for i in range(len(books_vt)):
    book_string = u''
    f1 = open('by_book/'+books_vt[i]+'.txt','w+',encoding='utf-8')
    for j in range(1,chapters_vt[i]+1):
        f2 = open('by_chapter/'+books_vt[i]+str(j)+'.txt','w+',encoding='utf-8')
        chapter_text = u''
        verse_exists = True
        verse = 1
        while verse_exists:
            verse_text = u''
            print('{0} {1}:{2}'.format(books_vt[i], str(j), str(verse)))
            if not os.path.exists(os.path.abspath("by_verse/{0}{1}_{2}.txt".format(books_vt[i], str(j), str(verse)))):
                f3 = open("by_verse/{0}{1}_{2}.txt".format(books_vt[i], str(j), str(verse)), 'w+', encoding='utf-8')
                for v in versions_vt:
                    if verse_exists:
                        try:
                            get_url = url + v + '/' + quote(books_vt[i]) + '/' + str(j) + '/' + str(verse)
                            req = Request(get_url, headers={'User-Agent': 'Mozilla/71.0'})
                            webpage = urlopen(req).read()
                            print('Funcionou: ', get_url)
                            sopa = BeautifulSoup(webpage, 'html.parser')
                            visible_texts = filter(tag_visible, sopa.findAll(text=True))
                            text = u" ".join(t.strip() for t in visible_texts)
                            verse_text += text
                            # time.sleep(0.01)
                        except HTTPError:
                            verse_exists = False
                            f3.close()
                            os.remove("by_verse/{0}{1}_{2}.txt".format(books_vt[i], str(j), str(verse)))
                if verse_exists:
                    f3.write(verse_text)
                    chapter_text += verse_text
                    verse+=1
            else:
                verse += 1
        f2.write(chapter_text)
        book_string += chapter_text
        f2.close()
    f1.write(book_string)
    f1.close()'''
for i in range(len(books_nt)):
    book_string = u''
    f1 = open('by_book/'+books_nt[i]+'.txt','w+',encoding='utf-8')
    for j in range(1,chapters_nt[i]+1):
        f2 = open('by_chapter/'+books_nt[i]+str(j)+'.txt','w+',encoding='utf-8')
        chapter_text = u''
        verse_exists = True
        verse = 1
        while verse_exists:
            verse_text = u''
            print('{0} {1}:{2}'.format(books_nt[i], str(j), str(verse)))
            print(os.path.abspath("by_verse/{0}{1}_{2}.txt".format(books_nt[i], str(j), str(verse))))
            if not os.path.exists(os.path.abspath("by_verse/{0}{1}_{2}.txt".format(books_nt[i], str(j), str(verse)))):
                f3 = open("by_verse/{0}{1}_{2}.txt".format(books_nt[i], str(j), str(verse)), 'w+', encoding='utf-8')
                for v in versions_nt:
                    if verse_exists:
                        try:
                            get_url = url + v + '/' + quote(books_nt[i]) + '/' + str(j) + '/' + str(verse)
                            req = Request(get_url, headers={'User-Agent': 'Mozilla/71.0'})
                            webpage = urlopen(req).read()
                            print('Funcionou: ', get_url)
                            sopa = BeautifulSoup(webpage, 'html.parser')
                            visible_texts = filter(tag_visible, sopa.findAll(text=True))
                            text = u" ".join(t.strip() for t in visible_texts)
                            verse_text += text
                            # time.sleep(0.01)
                        except HTTPError:
                            verse_exists = False
                            f3.close()
                            os.remove("by_verse/{0}{1}_{2}.txt".format(books_nt[i], str(j), str(verse)))
                if verse_exists:
                    f3.write(verse_text)
                    chapter_text += verse_text
                    verse+=1
            else:
                verse += 1
        f2.write(chapter_text)
        book_string += chapter_text
        f2.close()
    f1.write(book_string)
    f1.close()
