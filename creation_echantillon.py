import os
import random
import shutil


def creation_echantillon_mails (tailleEchantillon, nbEchantillon) :
    """Création d'un échantillon de mails parmis tous les mails récupérés dans le brief"""
    print ('\nCréation de', nbEchantillon, 'échantillons de', tailleEchantillon, 'mails...\n')

    # Définition des différents répertoires
    dirname = os.getcwd()
    mailDir = os.path.join(dirname,'maildir')

    # Comptage des emails
    mails_count = sum(len(files) for _, _, files in os.walk(mailDir)) 

    # On purge le dossier cible
    shutil.rmtree(os.path.join(dirname,'echantillons'))

    for echantillon in range(1, nbEchantillon+1) :
        print ('Echantillon numéro', echantillon)
        echantillonDir = os.path.join(dirname,'echantillons', str(echantillon))

        if not os.path.exists(echantillonDir):
            os.makedirs(echantillonDir)

        # On pioche 10K mails aléatoires et on les copie dans le dossier échantillon
        liste_rand = []
        for n in range(tailleEchantillon) :
            liste_rand.append(random.randint(0,mails_count))
        id_mail = 0
        for repertoire, sousRepertoires, fichiers in os.walk(mailDir):
            for f in fichiers :
                if id_mail in liste_rand :
                    shutil.copy(os.path.join(repertoire, f), echantillonDir)
                    liste_rand.remove(id_mail)
                id_mail +=1
        print ("Création de l'échantillon", echantillon, "réalisé avec succès :")
        print (tailleEchantillon, "mails aléatoires ont été copiés dans le répertoire cible.\n")
    
    print ('OK -', nbEchantillon, "de", tailleEchantillon, 'créé(s) dans le(s) répertoire(s) cible(s).')


creation_echantillon_mails(15, 3)


