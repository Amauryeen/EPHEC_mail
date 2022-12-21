import sys, os
from dotenv import load_dotenv

load_dotenv()

class NotAvalidChoice(Exception):
    pass


class App():

    @staticmethod
    def menu():
        print("\n-----   Menu   -----\n")
        print("1. Envoyer un mail")
        print("2. Récupérer mail serveur distant")
        print("3. Afficher mail")
        print("4. Quitter")
    
    @classmethod
    def create_mail(cls):
        from main import Mail
        total_input = []
        receivers = input("Entrez le/les destinataire(s) séparé par un espace : ").split(" ")
        sender=os.getenv('OUTLOOK_EMAIL')
        cc= input("Entrez le/les destinataire(s) en copie,  séparé par un espace : ").split(" ") 
        bcc= input("Entrez le/les destinataire(s) en copie cachée, séparé par un espace : ").split(" ")
        subject= input("Entrez le sujet de votre mail: ")
        print("Entrez votre message: ")
        while True:
            body= input()
            if body:
                total_input.append(body)
            else:
                break
        return Mail(receivers, sender, subject, total_input, cc, bcc)
    
    @staticmethod
    def menu_choice():
        menu_choice = int(input("\nQuelle est le numéro de votre choix : "))

        if menu_choice not in range(1, 5):
            raise NotAvalidChoice("Choice must be between 1 and 4")

        if menu_choice == 1:
            mail = App.create_mail()
            mail.send_mail()
        if menu_choice == 2:
            print("Nous avons récupéré votre courrier")
        if menu_choice == 3:
            print("Voici vos email")
        if menu_choice == 4:
            print("Au revoir!")
            sys.exit()