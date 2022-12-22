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
            receivers = input("Entrez le/les destinataire(s) séparé par un espace : ").split(" ")
            cc = input("Entrez le/les destinataire(s) en copie,  séparé par un espace : ").split(" ")
            if cc[0] == "":
                cc = []
            bcc = input("Entrez le/les destinataire(s) en copie cachée, séparé par un espace : ").split(" ")
            if bcc[0] == "":
                bcc = []
            subject = input("Entrez le sujet de votre mail: ")
            body = ""
            print("Entrez votre message: ")
            while True:
                body_part = input()
                if body_part:
                    body += body_part + "\n"
                else:
                    break
            try:
                mail = Mail(receivers, subject, body, cc, bcc)
                mail.send_mail()
                App.menu()
                App.menu_choice()

            except OSError as error:
                print(error)
                App.menu()
                App.menu_choice()

            except smtplib.SMTPServerDisconnected as error:
                print(error)
                App.menu()
                App.menu_choice()
            
            except smtplib.SMTPResponseException as error:
                print(error)
                App.menu()
                App.menu_choice()

            except smtplib.SMTPSenderRefused as error:
                print(error)
                App.menu()
                App.menu_choice()

            except smtplib.SMTPRecipientsRefused as error:
                print(error)
                App.menu()
                App.menu_choice()

            except smtplib.SMTPDataError as error:
                print(error)
                App.menu()
                App.menu_choice()

            except smtplib.SMTPConnectError as error:
                print(error)
                App.menu()
                App.menu_choice()

            except smtplib.SMTPHeloError as error:
                print(error)
                App.menu()
                App.menu_choice()

            except smtplib.SMTPNotSupportedError as error:
                print(error)
                App.menu()
                App.menu_choice()
            
            except smtplib.SMTPAuthenticationError as error:
                print(error)
                App.menu()
                App.menu_choice()

            except TimeoutError as error:
                print(error)
                App.menu()
                App.menu_choice()

        if menu_choice == 2:
            try:
                mail_box = MailBox()
                mail_box.get_mail()
                App.menu()
                App.menu_choice()
            
            except poplib.error_proto as error:
                print(error)
                App.menu()
                App.menu_choice()
            except OSError as error:
                print(error)
                App.menu()
                App.menu_choice()
            except TimeoutError as error:
                print(error)
                App.menu()
                App.menu_choice()
        if menu_choice == 3:
            print("Au revoir!")
            sys.exit()
