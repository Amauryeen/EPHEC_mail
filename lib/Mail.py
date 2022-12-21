import smtplib
from email.message import EmailMessage
import os
import re
from dotenv import load_dotenv

from lib.Exceptions import *

load_dotenv()


def check_mail(mail):
    """Vérifie que l'adresse mail est correctement formée

    PRE: mail est une adresse mail
    POST: retourne un boolean

    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, mail)


def check_sender(sender):
    """
    Vérifie que le sender est correct

    PRE: sender est un string, e-mail valide
    POST: ne renvoie rien
    RAISES: exception si PRE non-respecté

    :param sender:
    """
    if not isinstance(sender, str):
        raise InvalidType('Sender must be a string.')
    elif not check_mail(sender):
        raise InvalidMail(f'Sender "{sender}" is not a valid e-mail address.')


def check_receivers(receivers):
    """
    Vérifie que les receivers sont corrects

    PRE: sender est une liste, tous e-mails valides, 1 entrée minimum et 100 maximum
    POST: ne renvoie rien
    RAISES: exception si PRE non-respecté

    :param receivers:
    """
    if not isinstance(receivers, list):
        raise InvalidType('Receivers must be a list.')
    elif len(receivers) < 1:
        raise InvalidSize('Receivers must have at least 1 entry.')
    elif len(receivers) > 100:
        raise InvalidSize('Receivers must not exceed 100 entries.')

    for v in receivers:
        if not check_mail(v):
            raise InvalidMail(f'Entry "{v}" in Receivers is not a valid e-mail address.')


def check_subject(subject):
    """
    Vérifie que le subject est correct

    PRE: subject est un string, 200 caractères maximum
    POST: ne renvoie rien
    RAISES: exception si PRE non-respecté

    :param subject:
    """
    if not isinstance(subject, str):
        raise InvalidType('Subject must be a string.')
    elif len(subject) > 200:
        raise TooManyCharacters('Subject cannot exceed 200 characters.')


def check_body(body):
    """
    Vérifie que le body est correct

    PRE: body est un string, 1000 caractères maximum
    POST: ne renvoie rien
    RAISES: exception si PRE non-respecté

    :param body:
    """
    if not isinstance(body, str):
        raise InvalidType('Body must be a string.')
    elif len(body) > 1000:
        raise TooManyCharacters('Body cannot exceed 1000 characters.')


def check_cc(cc):
    """
    Vérifie que les cc sont corrects

    PRE: cc est une liste, tous e-mails valides, 100 entrées maximum
    POST: ne renvoie rien
    RAISES: exception si PRE non-respecté

    :param cc:
    """
    if not isinstance(cc, list):
        raise InvalidType('Cc must be a list.')
    elif len(cc) > 100:
        raise InvalidSize('Cc must not exceed 100 entries.')

    for v in cc:
        if len(cc) != 0 and not check_mail(v):
            raise InvalidMail(f'Entry "{v}" in Cc is not a valid e-mail address.')


def check_bcc(bcc):
    """
    Vérifie que les bcc sont corrects

    PRE: sender est une liste, tous e-mails valides, 100 entrées maximum
    POST: ne renvoie rien
    RAISES: exception si PRE non-respecté

    :param bcc:
    """
    if not isinstance(bcc, list):
        raise InvalidType('Bcc must be a list.')
    elif len(bcc) > 100:
        raise InvalidSize('Bcc must not exceed 100 entries.')

    for v in bcc:
        if len(bcc) != 0 and not check_mail(v):
            raise InvalidMail(f'Entry "{v}" in Bcc is not a valid e-mail address.')


class Mail:
    """Structure d'un mail contenant tout son contenu"""

    def __init__(self, receivers, subject="", body="", cc=None, bcc=None, sender=os.getenv('OUTLOOK_EMAIL')):
        """Initie un mail

        PRE: tous les arguments obligatoires sont présents, et les arguments présents sont corrects
        POST: initie la classe avec les champs spécifiés
        RAISES: renvoie une erreur si un des champs est incorrect, avec sa déscription

        """

        if bcc is None:
            bcc = []
        if cc is None:
            cc = []

        # Check if sender is valid
        check_sender(sender)

        # Check if receivers is valid
        check_receivers(receivers)

        # Check if subject is valid
        check_subject(subject)

        # Check if body is valid
        check_body(body)

        # Check if cc is valid
        check_cc(cc)

        # Check if bcc is valid
        check_bcc(bcc)

        self.__sender = sender
        self.__receivers = receivers
        self.__subject = subject
        self.__body = body
        self.__cc = cc
        self.__bcc = bcc

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
        """"Envoie un mail au(x) déstinataire(s)

        PRE: self possède chacun des champs obligatoires
        POST: affiche un message de succès dans la console si l'envoi réussit

        """
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
