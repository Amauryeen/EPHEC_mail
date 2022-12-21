from main import Mail
import os


class Mailbox(Mail):
    @classmethod
    def create_mail(cls):
        total_input = []
        receivers = input("Entrez le/les destinataire(s) séparé par un espace : ").split(" ")
        sender = os.getenv('OUTLOOK_EMAIL')
        cc = input("Entrez le/les destinataire(s) en copie,  séparé par un espace : ").split(" ")
        bcc = input("Entrez le/les destinataire(s) en copie cachée, séparé par un espace : ").split(" ")
        subject = input("Entrez le sujet de votre mail: ")
        print("Entrez votre message: ")
        while True:
            body = input()
            if body:
                total_input.append(body)
            else:
                break
        return Mail(receivers, sender, subject, total_input, cc, bcc)
