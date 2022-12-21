import os
import poplib
import email
from email.policy import default as default_policy


class MailBox:
    """Permet de récupérer tous les mails stockés sur le serveur distant"""
    def __init__(self):
        self.__login = os.getenv('OUTLOOK_EMAIL')
        self.__password = os.getenv('OUTLOOK_PASSWORD')
        self.__pop_server = os.getenv('POP_HOST')
        self.__pop_port = int(os.getenv('POP_PORT'))

    def get_mail(self):
        """Récupère tous les mails sur le serveur distant et les affiche en console un par un"""
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
            if body[1]:
                print(f"\tMessage: \n\n{body[1].decode('utf-8')}")
            else:
                print(f"\tMessage: \n\nNone")
            print("\n-----------------------------------------------\n")

        mail_box.quit()
