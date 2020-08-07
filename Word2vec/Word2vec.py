"""import nltk
import gensim
from nltk.corpus import abc

#nltk.download('abc')
nltk.download('punkt')

model= gensim.models.Word2Vec(abc.sents())
X= list(model.wv.vocab)
data=model.most_similar('money')
print(data)"""


from gensim.models import KeyedVectors
# load the google word2vec model
filename = 'GoogleNews-vectors-negative300.bin'
model = KeyedVectors.load_word2vec_format(filename, binary=True)
# calculate: (king - man) + woman = ?
#result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
result = model.similarity('lion', 'lions')
print(result)


"""import gensim.downloader as api

wv = api.load('word2vec-google-news-300')

vec_king = wv['king']

print(vec_king)"""