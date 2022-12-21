import smtplib
from email.message import EmailMessage
import poplib
import re
import os
from dotenv import load_dotenv
from app import App
from app import NotAValidChoice

load_dotenv()

class NotAValidChoice(Exception):
    pass


class TooManyCharacters(Exception):
    pass


class InvalidType(Exception):
    pass


class InvalidSize(Exception):
    pass


class InvalidMail(Exception):
    pass


def check_mail(mail):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, mail)


class Mail:

    def __init__(self):
        self.__receivers = input("Entrez le/les destinataire(s) séparé par un espace : ").split(" ")
        self.__sender = os.getenv('OUTLOOK_EMAIL')
        self.__cc= input("Entrez le/les destinataire(s) en copie,  séparé par un espace : ").split(" ")
        if self.__cc[0] == "":
            self.__cc = []
        self.__bcc= input("Entrez le/les destinataire(s) en copie cachée, séparé par un espace : ").split(" ")
        if self.__bcc[0] == "":
            self.__bcc = []
        self.__subject = input("Entrez le sujet de votre mail: ")
        self.__body = ""
        print("Entrez votre message: ")
        while True:
            body_part= input()
            if body_part:
                self.__body += body_part + "\n"
            else:
                break

        # Check if receivers is valid
        # TODO: receivers is a list, has at least 1 entry and maximum 100 entries, all entries are e-mails
        if not isinstance(self.receivers, list):
            raise InvalidType('Receivers must be a list.')
        elif len(self.receivers) < 1:
            raise InvalidSize('Receivers must have at least 1 entry.')
        elif len(self.receivers) > 100:
            raise InvalidSize('Receivers must not exceed 100 entries.')

        for v in self.receivers:
            if not check_mail(v):
                raise InvalidMail(f'Entry "{v}" in Receivers is not a valid e-mail address.')

        # Check if subject is valid
        # TODO: subject is less than 201 characters
        if not isinstance(self.subject, str):
            raise InvalidType('Subject must be a string.')
        elif len(self.subject) > 200:
            raise TooManyCharacters('Subject cannot exceed 200 characters.')

        # Check if body is valid
        # TODO: body is less than 1001 characters
        if not isinstance(self.subject, str):
            raise InvalidType('Body must be a string.')
        elif len(self.body) > 1000:
            raise TooManyCharacters('Body cannot exceed 1000 characters.')

        # Check if cc is valid
        # TODO: cc is a list, has a maximum of 100 entries, all entries are e-mails
        if not isinstance(self.cc, list):
            raise InvalidType('Cc must be a list.')
        elif len(self.cc) > 100:
            raise InvalidSize('Cc must not exceed 100 entries.')

        for v in self.cc:
            print(self.cc)
            print(len(self.cc))
            if len(self.cc) != 0 and not check_mail(v):
                raise InvalidMail(f'Entry "{v}" in Cc is not a valid e-mail address.')

        # Check if bcc is valid
        # TODO: bcc is a list, has a maximum of 100 entries, all entries are e-mails
        if not isinstance(self.bcc, list):
            raise InvalidType('Bcc must be a list.')
        elif len(self.bcc) > 100:
            raise InvalidSize('Bcc must not exceed 100 entries.')

        for v in self.bcc:
            if len(self.bcc) !=0 and not check_mail(v):
                raise InvalidMail(f'Entry "{v}" in Bcc is not a valid e-mail address.')


    # PROPERTIES

    @property
    def sender(self):
        return self.__sender

    @property
    def receivers(self):
        return self.__receivers

    @property
    def subject(self):
        return self.__subject

    @property
    def body(self):
        return self.__body

    @property
    def cc(self):
        return self.__cc

    @property
    def bcc(self):
        return self.__bcc

    # METHODS

    def send_mail(self):
        msg = EmailMessage()
        msg.set_content(self.body)
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = self.receivers
        msg['Cc'] = self.cc
        msg['Bcc'] = self.bcc

        with smtplib.SMTP(os.getenv('SMTP_HOST'), int(os.getenv('SMTP_PORT'))) as smtp:
            smtp.starttls()
            smtp.login(os.getenv('OUTLOOK_EMAIL'), os.getenv('OUTLOOK_PASSWORD'))
            smtp.send_message(msg)
            print("[+] Message sent succesfully...")
            smtp.quit()


class App():

    @staticmethod
    def menu():
        print("\n-----   Menu   -----\n")
        print("1. Envoyer un mail")
        print("2. Récupérer mail serveur distant")
        print("3. Afficher mail")
        print("4. Quitter")
    
    
    @staticmethod
    def menu_choice():
        menu_choice = int(input("\nQuelle est le numéro de votre choix : "))

        if menu_choice not in range(1, 5):
            raise NotAValidChoice("Choice must be between 1 and 4")

        if menu_choice == 1:
            mail = Mail()
            mail.send_mail()
            App.menu()
            App.menu_choice()
        if menu_choice == 2:
            print("Nous avons récupéré votre courrier")
        if menu_choice == 3:
            print("Voici vos email")
        if menu_choice == 4:
            print("Au revoir!")
            sys.exit()



def main():
    pass


if __name__ == "__main__":
    App.menu()
    while True:
        try:
            App.menu_choice()
            break

        except NotAValidChoice as error:
            print(f"[!] : {error}")
        except ValueError as error:
            print(f"[!] : {error}")