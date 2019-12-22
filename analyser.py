from sklearn.feature_extraction.text import CountVectorizer
import os
books_texts = {};
for path in os.listdir('by_book'):
	f = open('by_book\\'+path, 'r', encoding='utf-8');
	books_texts[path] = f.read();
	f.close();
chapters_texts = {};
for path in os.listdir('by_chapter'):
	f = open('by_chapter\\'+path, 'r', encoding='utf-8');
	chapters_texts[path] = f.read();
	f.close();
# list of text documents
full_text = [v for v in books_texts.values()]
# create the transform
vectorizer = CountVectorizer()
# tokenize and build vocab
vectorizer.fit(full_text)
# summarize
print(vectorizer.vocabulary_)
# encode documents
#vector = vectorizer.transform(text)
# summarize encoded vector
#print(vector.shape)
#print(type(vector))
#print(vector.toarray())