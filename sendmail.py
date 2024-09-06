import base64
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import smtplib
import os
from creds import *

file_path = r'{PATH}'

email = email
password = password

def sendmail(from_, date):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(user=email, password=password)

    attachment = r'{PATH}/output.wav'

    msg = MIMEMultipart()
    msg['Subject'] = "NOOZ" + date
    msg.attach(MIMEText("Here is your daily news podcast:"))

    with open('output.wav', 'rb') as f:
        file = MIMEBase("application", "octet-stream")
        file.set_payload(f.read())

    encode_base64(file)

    file['Content-Disposition'] = f'attachment;\
    filename="{os.path.basename(attachment)}"'

    msg.attach(file)

    smtp.sendmail(from_addr=email,
                  to_addrs=[from_],
                  msg=msg.as_string())

    print("sent")

    smtp.quit()
