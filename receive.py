#!/usr/bin/env python3

import email, poplib
import os, sys
import socket
from dotenv import load_dotenv
from email.policy import default as default_policy

load_dotenv()


login = os.getenv('OUTLOOK_EMAIL')
password = os.getenv('OUTLOOK_PASSWORD')
pop_server = 'outlook.office365.com'
pop_port = 995


try:
    mail_box = poplib.POP3_SSL(pop_server, pop_port)
    mail_box.user(login)
    mail_box.pass_(password)
    print("[+] Connection established...\n")

except poplib.error_proto as error:
    print(error)
    sys.exit()
except OSError as error:
    print(error)
    sys.exit()
except TimeoutError as error:
    print(error)
    sys.exit()

num_messages = len(mail_box.list()[1])

for i in range(1, num_messages + 1):
    body = []
    print(f"message {i}:")

    raw_email  = b"\n".join(mail_box.retr(i)[1])
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