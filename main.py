import smtplib
from email.message import EmailMessage
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

    def __init__(self, receivers, sender=os.getenv('OUTLOOK_EMAIL'), subject='', body='', cc=None, bcc=None):
        if cc is None:
            cc = []
        if bcc is None:
            bcc = []

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
                raise NotMail(f'Entry "{v}" in Receivers is not a valid e-mail address.')

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
        if not isinstance(cc, list):
            raise InvalidType('Cc must be a list.')
        elif len(cc) > 100:
            raise InvalidSize('Cc must not exceed 100 entries.')

        for v in cc:
            if not check_mail(v):
                raise NotMail(f'Entry "{v}" in Cc is not a valid e-mail address.')

        # Check if bcc is valid
        # TODO: bcc is a list, has a maximum of 100 entries, all entries are e-mails
        if not isinstance(bcc, list):
            raise InvalidType('Bcc must be a list.')
        elif len(bcc) > 100:
            raise InvalidSize('Bcc must not exceed 100 entries.')

        for v in bcc:
            if not check_mail(v):
                raise NotMail(f'Entry "{v}" in Bcc is not a valid e-mail address.')

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
            smtp.quit()


def main():
    pass
