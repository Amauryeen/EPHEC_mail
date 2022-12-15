import smtplib
import poplib
import re
import os
from dotenv import load_dotenv

load_dotenv()


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

    def __init__(self, receivers, sender=os.getenv('OUTLOOK_EMAIL'), subject='', body='', cc=None, cci=None):
        if cc is None:
            cc = []
        if cci is None:
            cci = []

        # Amaury
        # Check if receivers is valid
        # TODO: receivers is a list, has at least 1 entry and maximum 100 entries, all entries are e-mails
        if not isinstance(receivers, list):
            raise InvalidType('Receivers must be a list.')
        elif len(receivers) < 1:
            raise InvalidSize('Receivers must have at least 1 entry.')
        elif len(receivers) > 100:
            raise InvalidSize('Receivers must not exceed 100 entries.')

        for v in receivers:
            if not check_mail(v):
                raise NotMail(f'Entry "{v}" in Receivers is not a valid mail address.')

        # Check if subject is valid
        # TODO: subject is less than 201 characters
        if not isinstance(subject, str):
            raise InvalidType('Subject must be a string.')
        elif len(subject) > 200:
            raise TooManyCharacters('Subject cannot exceed 200 characters.')

        # Check if body is valid
        # TODO: body is less than 1001 characters
        if not isinstance(subject, str):
            raise InvalidType('Body must be a string.')
        elif len(body) > 1000:
            raise TooManyCharacters('Body cannot exceed 1000 characters.')

        # Check if cc is valid
        # TODO: cc is a list, has a maximum of 100 entries, all entries are e-mails
        if not isinstance(receivers, list):
            raise InvalidType('Cc must be a list.')
        elif len(receivers) > 100:
            raise InvalidSize('Cc must not exceed 100 entries.')

        for v in cc:
            if not check_mail(v):
                raise NotMail(f'Entry "{v}" in Cc is not a valid mail address.')

        # Check if cci is valid
        # TODO: cci is a list, has a maximum of 100 entries, all entries are e-mails
        if not isinstance(receivers, list):
            raise InvalidType('Cci must be a list.')
        elif len(receivers) > 100:
            raise InvalidSize('Cci must not exceed 100 entries.')

        for v in cci:
            if not check_mail(v):
                raise NotMail(f'Entry "{v}" in Cci is not a valid mail address.')

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
