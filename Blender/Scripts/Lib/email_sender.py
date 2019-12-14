#! /usr/bin/env python
#coding=utf-8

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


class Email:
    def __init__(self):
        self.host_server = 'smtp.qq.com'
        self.sender = '841781063@qq.com'
        self.password = None
        self.receiver = None
        self.mail_content = None
        self.mail_title = "Render Task Done!"

    def send_email(self):
        # ssl
        smtp = SMTP_SSL(self.host_server)
        smtp.set_debuglevel(1)
        smtp.ehlo(self.host_server)
        smtp.login(self.sender, self.password)

        msg = MIMEText(self.mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(self.mail_title, 'utf-8')
        msg["From"] = self.sender
        msg["To"] = self.receiver
        smtp.sendmail(self.sender, self.receiver, msg.as_string())
        smtp.quit()