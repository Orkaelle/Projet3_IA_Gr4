#Recherche de synonymes de mots clés et catégorisation des résultats
#Auteur : Nicolas Campion
#Dernière mise à jour : 27 août 2020


import sys
import csv
import numpy
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from gensim.models import KeyedVectors


synonyms = []
contenuClusters = []
listeCategories = []

maxInt = sys.maxsize
divisionValeur = 0

#Permet d'instancier la taille maximale de la variable dédiée au fichier csv et éviter une saturation 
while True:
    divisionValeur += 1
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt / divisionValeur)

#Chargement du fichier permettant de comparer deux mots-clés
#Important : le fichier GoogleNews-vectors-negative300.bin doit être placé dans le même dossier (archive téléchargeable sur https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit)
filename = 'GoogleNews-vectors-negative300.bin'
model = KeyedVectors.load_word2vec_format(filename, binary=True)

#Lecture du fichier texte contenant les courriels
with open('dataset_10.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    documents  = [""]
    comptageLigne = 0
    for row in csv_reader:
        documents = numpy.append(documents, [row[3]])
        comptageLigne += 1
        documents = numpy.append(documents, [row[3]])
        comptageLigne += 1
csv_file.close()

#Initialisation de la liste des mots à igniorer lors de la recherche dans le fichier
listeCompleteMotsBloques = stopwords.words('english') + stopwords.words('spanish')
vectoriseur = TfidfVectorizer(stop_words=listeCompleteMotsBloques)
X = vectoriseur.fit_transform(documents)

#Initalisation de la recherche de clusters
nombreClusters = 100
modele = KMeans(n_clusters=nombreClusters, init='k-means++', max_iter=6000, n_init=1)
modele.fit(X)

ordreCentroides = modele.cluster_centers_.argsort()[:, ::-1]
termes = vectoriseur.get_feature_names()

#Détection des clusters et enregistrement dans le fichier motsClusters.csv
with open('motsClusters.csv', mode='w') as clusters_file:
    motsClusters = csv.writer(clusters_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')

    for i in range (nombreClusters):
        cluster = "Cluster %d:" % i
        for indic in ordreCentroides[i, :10]:
            valeur = termes[indic]
            if not valeur.isdigit():
                motsClusters.writerow([cluster, termes[indic]])
                contenuClusters = numpy.append(contenuClusters, [termes[indic]])
    
clusters_file.close()

#Recherche des synonymes, détection des catégories, filtrage par distinction, puis enregistrement dans le fichier motsSynonymes.csv
with open('motsSynonymes.csv', mode='w') as synonyms_file:
    motsSynonymes = csv.writer(synonyms_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')

    for i in range (0, len(contenuClusters)):
        for syn in wordnet.synsets(contenuClusters[i]):
            nomOrigine = contenuClusters[i]
            for l in syn.lemmas():
                motsSynonymes.writerow([nomOrigine, l.name()])

                try:
                    result = model.similarity(nomOrigine, l.name())
                    if (float(result) >= 0.99):
                        print (str(l.name()))
                        listeCategories = numpy.append(listeCategories, [l.name()])
                except:
                    print(str(nomOrigine) + " + " + str(l.name()) + " = echec")
    
    print (listeCategories)
    listeCategories = list(set(listeCategories))
    print (listeCategories)

synonyms_file.close()

# Comparaison des mots, regroupement par catégorie, puis enregistrement dans le fichier motsCategories.csv
with open('motsCategories.csv', mode='w') as categories_file:
    motsCategories = csv.writer(categories_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')

    for i in range (0, len(listeCategories)):
        for syn in wordnet.synsets(str(listeCategories[i])):
            motcategorie = listeCategories[i]
            for l in syn.lemmas():
                try:
                    result = model.similarity(motcategorie, l.name())
                    if (float(result) >= 0.2 and float(result) < 0.99):
                        motsCategories.writerow([motcategorie, l.name()])
                except:
                    print(str(motcategorie) + " + " + str(l.name()) + " = echec")
    
categories_file.close()