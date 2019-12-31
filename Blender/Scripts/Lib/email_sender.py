#! /usr/bin/env python
#coding=utf-8

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from smtplib import SMTP_SSL


class Email:
    def __init__(self):
        self.host_server = 'smtp.qq.com'
        self.sender = '841781063@qq.com'
        self.password = None
        self.receiver = None
        self.mail_content = None
        self.image_path = None
        self.video_path = None
        self.mail_title = "Render Task Done!"
        self.video_name = "video.mp4"

    def send_email(self):
        # ssl
        smtp = SMTP_SSL(self.host_server)
        smtp.set_debuglevel(1)
        smtp.ehlo(self.host_server)
        smtp.login(self.sender, self.password)

        message = MIMEMultipart('mixed')
        # text
        message.attach(MIMEText(self.mail_content, "plain", "utf-8"))
        message["From"] = self.sender
        message["To"] = self.receiver
        message["Subject"] = Header(self.mail_title, 'utf-8')
        # video attachment
        att1 = MIMEText(open(self.video_path, "rb").read(), "base64", "utf-8")
        att1["Content-Type"] = "video/mp4"
        att1["Content-Disposition"] = "attachment;filename=" + self.video_name
        message.attach(att1)

        # image
        att2 = MIMEImage(open(self.image_path, 'rb').read())
        att2.add_header('Content-ID', '<image1>')
        message.attach(att2)

        smtp.sendmail(self.sender, self.receiver, message.as_string())
        smtp.quit()