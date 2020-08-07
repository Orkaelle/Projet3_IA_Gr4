"""import nltk
nltk.download('omw')"""

from nltk.corpus import wordnet
synonyms = []
antonyms = []

for syn in wordnet.synsets("good"):
    for l in syn.lemmas():
        synonyms.append(l.name())
print("\nSet of synonyms in English :")
print(set(synonyms))

for syn in wordnet.synsets("bueno",lang=('spa')):
    for l in syn.lemmas():
        synonyms.append(l.name())
print("\nSet of synonyms in Spanish :")
print(set(synonyms))