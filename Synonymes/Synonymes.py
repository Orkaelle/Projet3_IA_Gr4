"""import nltk
nltk.download('wordnet')"""

from nltk.corpus import wordnet
synonyms = []
#antonyms = []

for syn in wordnet.synsets("end"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        """if l.antonyms():
            antonyms.append(l.antonyms()[0].name())"""
print("\nSet of synonyms of the said word:")
print(set(synonyms))
"""print("\nSet of antonyms of the said word:")
print(set(antonyms))"""