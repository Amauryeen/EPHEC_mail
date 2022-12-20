#!/usr/bin/env python3

import email, poplib
import mailbox
from email.header import decode_header
import os
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

except poplib.error_proto as error:
    print(error)

print(mail_box.list())
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
    print(f"\tMessage: \n{body[1].decode('utf-8')}")

mail_box.quit()