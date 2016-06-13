#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
import sys

# seperate mailing_list information and gmail account from here
# mailing_list is list, ex mailing_list = [ "a@gmail.com", "b@gmail.com" ]
# account is gmail login information, account.xuser = "a@gamil.com", account.xpass = "xxx"
import mailing_list
import account as g

def send_mail(subject, attach, to, text):
	msg = MIMEMultipart()

	msg['From'] = g.xuser
	msg['Subject'] = subject

	msg.attach(MIMEText(text))

	part = MIMEBase('application', 'octet-stream')
	part.set_payload(open(attach, 'rb').read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attach))
	msg.attach(part)

	mailServer = smtplib.SMTP("smtp.gmail.com", 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(g.xuser, g.xpass)
	mailServer.sendmail(g.xuser, to, msg.as_string())

	mailServer.close()

if __name__ == '__main__':
	# test code
	if sys.argv[1]:
		send_mail('python test 5', sys.argv[1], mailing_list.mailing_list, 'test purpose')
