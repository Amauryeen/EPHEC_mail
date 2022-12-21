import smtplib
import email
import socket
from email.policy import default as default_policy
from email.message import EmailMessage
import poplib
import re
import os
from dotenv import load_dotenv


load_dotenv()


class NotAvalidChoice(Exception):
    pass


class TooManyCharacters(Exception):
    pass


class InvalidType(Exception):
    pass


class InvalidSize(Exception):
    pass


class NotMail(Exception):
    pass


def check_mail(mail):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, mail)


class Mail:

    def __init__(self):
        self.__receivers = input("Entrez le/les destinataire(s) séparé par un espace : ").split(" ")
        self.__sender = os.getenv('OUTLOOK_EMAIL')
        self.__cc = input("Entrez le/les destinataire(s) en copie,  séparé par un espace : ").split(" ")
        if self.__cc[0] == "":
            self.__cc = []
        self.__bcc = input("Entrez le/les destinataire(s) en copie cachée, séparé par un espace : ").split(" ")
        if self.__bcc[0] == "":
            self.__bcc = []
        self.__subject = input("Entrez le sujet de votre mail: ")
        self.__body = ""
        print("Entrez votre message: ")
        while True:
            body_part = input()
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
                raise NotMail(f'Entry "{v}" in Receivers is not a valid e-mail address.')

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
                raise NotMail(f'Entry "{v}" in Cc is not a valid e-mail address.')

        # Check if bcc is valid
        # TODO: bcc is a list, has a maximum of 100 entries, all entries are e-mails
        if not isinstance(self.bcc, list):
            raise InvalidType('Bcc must be a list.')
        elif len(self.bcc) > 100:
            raise InvalidSize('Bcc must not exceed 100 entries.')

        for v in self.bcc:
            if len(self.bcc) != 0 and not check_mail(v):
                raise NotMail(f'Entry "{v}" in Bcc is not a valid e-mail address.')

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


class App:

    @staticmethod
    def menu():
        print("\n-----   Menu   -----\n")
        print("1. Envoyer un mail")
        print("2. Afficher mail")
        print("3. Quitter")

    @staticmethod
    def menu_choice():
        menu_choice = int(input("\nQuelle est le numéro de votre choix : "))

        if menu_choice not in range(1, 5):
            raise NotAvalidChoice("Choice must be between 1 and 4")

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


class MailBox:
    def __init__(self):
        self.__login = os.getenv('OUTLOOK_EMAIL')
        self.__password = os.getenv('OUTLOOK_PASSWORD')
        self.__pop_server = 'outlook.office365.com'
        self.__pop_port = 995

    def get_mail(self):        
        mail_box = poplib.POP3_SSL(self.__pop_server, self.__pop_port)
        mail_box.user(self.__login)
        mail_box.pass_(self.__password)
        print("[+] La connection avec le serveur pop distant est établie...\n")
        num_messages = len(mail_box.list()[1])

        for i in range(1, num_messages + 1):
            body = []
            print(f"message {i}:")

            raw_email = b"\n".join(mail_box.retr(i)[1])
            parsed_email = email.message_from_bytes(raw_email, policy=email.policy.default)
            print(f"\tSubject: {parsed_email['Subject']}")
            print(f"\tFrom: {parsed_email['From']}")
            print(f"\tDate: {parsed_email['Date']}")
            for part in parsed_email.walk():
                if part.get_content_type():

                    body.append(part.get_payload(decode=True))
            print(f"\tMessage: \n\n{body[1].decode('utf-8')}")
            print("\n-----------------------------------------------\n")

        mail_box.quit()


if __name__ == "__main__":
    App.menu()
    while True:
        try:
            App.menu_choice()
            break

        except NotAvalidChoice as error:
            print(f"[!] : {error}")
        except ValueError as error:
            print(f"[!] : {error}")
import smtplib
import email
import socket
from email.policy import default as default_policy
from email.message import EmailMessage
import poplib
import re
import os
from dotenv import load_dotenv


load_dotenv()


class NotAvalidChoice(Exception):
    pass


class TooManyCharacters(Exception):
    pass


class InvalidType(Exception):
    pass


class InvalidSize(Exception):
    pass


class NotMail(Exception):
    pass


def check_mail(mail):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, mail)


class Mail:

    def __init__(self):
        self.__receivers = input("Entrez le/les destinataire(s) séparé par un espace : ").split(" ")
        self.__sender = os.getenv('OUTLOOK_EMAIL')
        self.__cc = input("Entrez le/les destinataire(s) en copie,  séparé par un espace : ").split(" ")
        if self.__cc[0] == "":
            self.__cc = []
        self.__bcc = input("Entrez le/les destinataire(s) en copie cachée, séparé par un espace : ").split(" ")
        if self.__bcc[0] == "":
            self.__bcc = []
        self.__subject = input("Entrez le sujet de votre mail: ")
        self.__body = ""
        print("Entrez votre message: ")
        while True:
            body_part = input()
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
                raise NotMail(f'Entry "{v}" in Receivers is not a valid e-mail address.')

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
                raise NotMail(f'Entry "{v}" in Cc is not a valid e-mail address.')

        # Check if bcc is valid
        # TODO: bcc is a list, has a maximum of 100 entries, all entries are e-mails
        if not isinstance(self.bcc, list):
            raise InvalidType('Bcc must be a list.')
        elif len(self.bcc) > 100:
            raise InvalidSize('Bcc must not exceed 100 entries.')

        for v in self.bcc:
            if len(self.bcc) != 0 and not check_mail(v):
                raise NotMail(f'Entry "{v}" in Bcc is not a valid e-mail address.')

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


class App:

    @staticmethod
    def menu():
        print("\n-----   Menu   -----\n")
        print("1. Envoyer un mail")
        print("2. Afficher mail")
        print("3. Quitter")

    @staticmethod
    def menu_choice():
        menu_choice = int(input("\nQuelle est le numéro de votre choix : "))

        if menu_choice not in range(1, 5):
            raise NotAvalidChoice("Choice must be between 1 and 4")

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


class MailBox:
    def __init__(self):
        self.__login = os.getenv('OUTLOOK_EMAIL')
        self.__password = os.getenv('OUTLOOK_PASSWORD')
        self.__pop_server = 'outlook.office365.com'
        self.__pop_port = 995

    def get_mail(self):        
        mail_box = poplib.POP3_SSL(self.__pop_server, self.__pop_port)
        mail_box.user(self.__login)
        mail_box.pass_(self.__password)
        print("[+] La connection avec le serveur pop distant est établie...\n")
        num_messages = len(mail_box.list()[1])

        for i in range(1, num_messages + 1):
            body = []
            print(f"message {i}:")

            raw_email = b"\n".join(mail_box.retr(i)[1])
            parsed_email = email.message_from_bytes(raw_email, policy=email.policy.default)
            print(f"\tSubject: {parsed_email['Subject']}")
            print(f"\tFrom: {parsed_email['From']}")
            print(f"\tDate: {parsed_email['Date']}")
            for part in parsed_email.walk():
                if part.get_content_type():

                    body.append(part.get_payload(decode=True))
            print(f"\tMessage: \n\n{body[1].decode('utf-8')}")
            print("\n-----------------------------------------------\n")

        mail_box.quit()


if __name__ == "__main__":
    App.menu()
    while True:
        try:
            App.menu_choice()
            break

        except NotAvalidChoice as error:
            print(f"[!] : {error}")
        except ValueError as error:
            print(f"[!] : {error}")
