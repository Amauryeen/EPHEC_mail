import smtplib
import poplib
import re

import os
from dotenv import load_dotenv
load_dotenv()


def check_mail(mail):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, mail)


class Mail:

    def __init__(self, receivers, sender=os.getenv('OUTLOOK_EMAIL'), subject='', body='', cc=None, cci=None):
        if cc is None:
            cc = []
        if cci is None:
            cci = []

        # Amaury
        # Check if receivers is valid
        # TODO: receivers is a list, has at least 1 entry and maximum 100 entries, all entries are e-mails

        # Check if subject is valid
        # TODO: subject is less than 201 characters

        # Check if body is valid
        # TODO: body is less than 1001 characters

        # Check if cc is valid
        # TODO: cc is a list, has a maximum of 100 entries, all entries are e-mails

        # Check if cci is valid
        # TODO: cci is a list, has a maximum of 100 entries, all entries are e-mails

        self.__sender = sender
        self.__receivers = receivers
        self.__subject = subject
        self.__body = body
        self.__cc = cc
        self.__cci = cci

    # PROPERTIES

    @property
    def sender(self):
        return self.__sender

    @property
    def receivers(self):
        return self.__receivers

    @property
    def sender(self):
        return self.__sender

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
    def cci(self):
        return self.__cci

    # METHODS

    def send_mail(self):
        # Amaury
        pass


def main():
    pass


if __name__ == '__main__':
    main()
