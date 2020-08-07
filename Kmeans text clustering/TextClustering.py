from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from nltk.corpus import stopwords

documents = ["This little kitty came to play when I was eating at a restaurant.",
             "Merley has the best squooshy kitten belly.",
             "Google Translate app is incredible.",
             "If you open 100 tab in google you get a smiley face.",
             "Best cat photo I've ever taken.",
             "Climbing ninja cat.",
             "Impressed with google map feedback.",
             "Key promoter extension for Google Chrome.",
             "Le tigre est en toi.",
             "La Virtual Boy fut un grand échec pour Nintendo et Gunpey Yokoi.",
             "Gunpey Yokoi a fortement contribué au succès de Nintendo en proposant bon nombre de jouets.",
             "Quand un loup s'en prend à un tigre déguisé en mouton, c'est souvent trop tard qu'il se rend compte de son erreur.",
             "Le tigre fait partie de la famille des félins.",
             "Mario est la mascotte de Nintendo.",
             "Le chat est un félin acceptant la compagnie de l'homme.",
             "Prend garde à Shere Khan, petit homme, répondit l'ami félin de Mowgli.",
             "El Gobierno estuvo al tanto pero la decisión final fue del Rey.",
             "El Gobierno libanés apunta a un cargamento de 2.750 toneladas de nitrato de amonio almacenado en el puerto como posible causa de la detonación.",
             "La falta de turistas internacionales en Madrid, la mayoría de origen asiático, tumba la economía de las marcas de lujo.",
             "Vox estrena su nuevo sindicato en el barrio de Salamanca",
             "La Corte Suprema de Colombia ordena la detención del expresidente Álvaro Uribe",
             "Cinco planes para perderse en el bosque en familia",
             "Banca digital: tendencias que marcarán el futuro de la industria",
             "La sencillez compleja del diseño de los coches eléctricos",
             "Los baobabs, los gigantes africanos y la pesadilla de ‘El Principito’",
             "Historias en profundidad para conocer, entender y actuar"]

listeCompleteMotsBloques = stopwords.words('english') + stopwords.words('spanish') + stopwords.words('french')
#vectorizer = TfidfVectorizer(stop_words='english')
vectoriseur = TfidfVectorizer(stop_words=listeCompleteMotsBloques)
X = vectoriseur.fit_transform(documents)

nombreClusters = 3
modele = KMeans(n_clusters=nombreClusters, init='k-means++', max_iter=100, n_init=1)
modele.fit(X)

print("Meilleurs termes par cluster:")
ordreCentroides = modele.cluster_centers_.argsort()[:, ::-1]
termes = vectoriseur.get_feature_names()
for i in range(nombreClusters):
    print("Cluster %d:" % i),
    for indic in ordreCentroides[i, :10]:
        print(' %s' % termes[indic]),
    print

"""print("\n")
print("Prediction")

Y = vectorizer.transform(["Le tigre est le plus grand félin au monde."])
prediction = model.predict(Y)
print(prediction)

Y = vectorizer.transform(["Nintendo domine les jeux vidéos."])
prediction = model.predict(Y)
print(prediction)"""