from lib.Exceptions import *
from lib.Mail import *
from lib.MailBox import *
import sys


class App:
    """Classe responsable de l'affichage du menu permettant la sélection de l'action à effectuer"""

    @staticmethod
    def menu():
        """Affichage du menu"""
        print("\n-----   Menu   -----\n")
        print("1. Envoyer un mail")
        print("2. Afficher mail")
        print("3. Quitter")

    @staticmethod
    def menu_choice():
        """Sélection après affichage du menu"""
        menu_choice = int(input("\nQuel est le numéro de votre choix : "))

        if menu_choice not in range(1, 5):
            raise NotAValidChoice("Choice must be between 1 and 4")

        if menu_choice == 1:
            mail = Mail()
            mail.send_mail()
            App.menu()
            App.menu_choice()
        if menu_choice == 2:
            try:
                mail_box = MailBox()
                mail_box.get_mail()
            except Exception as e:
                print(e)
        if menu_choice == 3:
            print("Au revoir!")
            sys.exit()
