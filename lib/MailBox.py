import os
import poplib
import email
from email.policy import default as default_policy

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
