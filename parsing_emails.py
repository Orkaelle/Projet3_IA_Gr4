import os
import mailparser
import csv

# recuperation du dossier du travail
dir_path = os.path.dirname(os.path.realpath(__file__))

""" recuperer les donneés depuis un email
return: objet json contenant le contenu d'un email
"""
def get_data_from_email(file):
    
    # initialisation de l'objet à retourner
    email_details = {
        'from': None,
        'to': [],
        'date': None,
        'subject': None,
        'body': None
    }

    # parser l'email
    mail = mailparser.parse_from_file(file)

    # l'emetteur de l'email
    email_details['from'] = mail.from_[0][1]
    
    # la liste des destinataires
    for i in range(0, len(mail.to)):
        email_details['to'].append(mail.to[i][1])
    
    # la date d'envoie de l'email
    email_details['date'] = mail.date

    # le sujet de l'email
    email_details['subject'] = mail.subject

    # le contenu de l'emamil
    email_details['body'] = mail.body

    return email_details


def append_email_to_csv(file):
    
    # recuperer le contenu de l'email
    email_details = get_data_from_email(file)

    # ouvrir le fichier dataset
    file_path = os.path.join(dir_path, 'dataset_brut.csv')
    with open(file_path, mode='a+', newline='') as csv_file:
        
        # definition des parametres du dictionnaire à enregistrer dans le fichier csv
        fieldnames = ['from', 'to','date', 'subject', 'body']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # ecriture du contenu de l'email dans le fichier csv
        writer.writerow(
            {
                'from': email_details['from'],
                'to': email_details['to'],
                'date': email_details['date'],
                'subject': email_details['subject'],
                'body': email_details['body']
                }
             )

"""fonction qui permet d'iterer un dossier contenant des fichiers d'emails
"""
def iterate_emails():
    file_path = os.path.join(dir_path, 'echantillons')
    for subdir, dirs, files in os.walk(file_path):
        for file in files:
            append_email_to_csv(os.path.join(subdir, file))

"""ecriture du fichier avant recuperation des données
"""
def write_dataset_file():
    file_path = os.path.join(dir_path, 'dataset_brut.csv')
    with open(file_path, mode='w+', newline='') as csv_file:
        fieldnames = ['from', 'to', 'date', 'subject', 'body']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

write_dataset_file()
iterate_emails()