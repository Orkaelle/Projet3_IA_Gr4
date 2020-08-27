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
        'message_id': None,
        'name': None,
        'from': None,
        'to': [],
        'date': None,
        'subject': None,
        'body': None
    }

    # parser l'email
    mail = mailparser.parse_from_file(file)
    
    # recuperer les infos de l'email
    email_details['message_id'] = mail.headers['Message-ID'] #mail.message_as_string.partition('\n')[0].partition(':')[2]
    email_details['name'] = mail.headers['X-From']
    email_details['from'] = mail.from_[0][1]   
    for i in range(0, len(mail.to)):
        email_details['to'].append(mail.to[i][1])
    
    email_details['date'] = mail.date
    email_details['subject'] = mail.subject if mail.subject else 'None'
    email_details['body'] = mail.body

    return email_details


"""enregistrer les infos de l'email dans le fichier csv
"""
def append_email_to_csv(directory, file):

    new_file = False

    # creation lien vers fichier dataset
    dir_basename = os.path.basename(os.path.normpath(directory))
    
    # creation de dossier de datasets
    directory_dataset = os.path.join(dir_path, 'datasets')   
    if not os.path.exists(directory_dataset):
        os.makedirs(directory_dataset)
    
    # lien du fichier dataset
    file_path = os.path.join(directory_dataset, f'dataset_{dir_basename}.csv')

    # creation du fichier s'il n'existe pas
    if not os.path.exists(file_path):
        print(f'creation dataset: {dir_basename}')
        new_file = True

    # recuperer le contenu de l'email
    email_details = get_data_from_email(file)

    # # ecriture des données dans le fichier
    with open(file_path, mode='a+', newline='') as csv_file:
        
        # definition des parametres du dictionnaire à enregistrer dans le fichier csv
        fieldnames = ['message_id', 'from', 'to','date', 'subject', 'body']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # creation des en-tetes si c'est un nouveau fichier
        if new_file:
            writer.writeheader()

        # ecriture du contenu de l'email dans le fichier csv
        writer.writerow(
            {
                'message_id': email_details['message_id'],
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
    echantillon_path = os.path.join(dir_path, 'echantillons')
    for subdir, dirs, files in os.walk(echantillon_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            append_email_to_csv(subdir, file_path)


def main():
    """Entrypoint to application."""
    iterate_emails()


if __name__ == '__main__':
    main()