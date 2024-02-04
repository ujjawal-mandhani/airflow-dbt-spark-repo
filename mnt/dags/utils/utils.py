import time
import email
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from airflow.models import Variable

sender_email =  Variable.get('sender_email')
password = Variable.get('sender_password')

def sender_email_function(receiver_email_arg, Subject, mess):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email_arg)
    message["Subject"] = Subject
    SUBJECT = Subject
    body = """<html>
                <head></head>
                <body>
                  <p> Email recieved successfully from Airflow</p>
                  <p> {}
                </body>
                </html>""".format(SUBJECT, mess)           
    message.attach(MIMEText(body, "html"))
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email_arg, text)