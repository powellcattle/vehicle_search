#!/usr/bin/python3
import json
import mimetypes
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage


class Mail:
    def __init__(self, port, smtp_server_domain_name, sender_mail, password):
        self.msg = EmailMessage()
        self.msg['Subject'] = 'Vehicle Reports'
        self.msg['Bcc'] = ','.join(['spowell@sbcglobal.net'])
        self.msg['From'] = 'spowell@powellcattle.com'
        self.port = port
        self.smtp_server_domain_name = smtp_server_domain_name
        self.sender_mail = sender_mail
        self.password = password

    def send(self):
        ssl_context = ssl.create_default_context()

        with smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context) as service:
            service.login(user=self.sender_mail, password=self.password)
            service.send_message(self.msg)


directory = '../../dev/reports/'
mail = ''
es = {}
try:
    f = open('meta-data/email_server.json')
    es = json.load(f)
    mail = Mail(port=es['port'],
                smtp_server_domain_name=es['smtp_server_domain_name'],
                sender_mail=es['sender_mail'],
                password=es['password'])

    f.close()
except OSError as e:
    sys.intern(e.strerror)

for filename in os.listdir(directory):
    mime_type = mimetypes.guess_type(filename)
    mime_type, mime_subtype = mime_type[0].split('/', 1)
    f = os.path.join(directory, filename)

    with open(f, 'rb') as ap:
        mail.msg.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype, filename=f)

mail.send()
