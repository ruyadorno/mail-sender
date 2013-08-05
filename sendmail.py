#!/usr/bin/env python

import argparse
import datetime
import smtplib
import base64

import config


# Add a nice helper description
DESCRIPTION = """Send an email using smtp and plain python.
SMTP settings can be added on config.py file;
The subject and email can be set on user input."""
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.parse_args()


def get_subject(subject):
    subject_base64 = base64.encodestring(subject).strip()
    return "=?UTF-8?B?%s?=" % subject_base64

def get_file():
    try:
        file = open(config.smtp_template, 'r')
    except IOError:
        print 'Template file does not exist.'
        exit()
    return file

def get_message(subject, mail_to):
    file = get_file()
    msg = file.read()
    msg = msg.replace('{{FROM_MAIL}}', config.smtp_mail) \
        .replace('{{FROM_NAME}}', config.smtp_name) \
        .replace('{{SUBJECT}}', subject) \
        .replace('{{TO_MAIL}}', mail_to)
    return msg

def smtp_mail(mail_to, message):
    smtpObj = smtplib.SMTP_SSL(config.smtp_address, config.smtp_port)
    smtp_login(smtpObj)
    sendmail(smtpObj, mail_to, message)

def smtp_login(smtp):
    try:
        smtp.login(config.smtp_mail, config.smtp_password)
    except smtplib.SMTPHeloError:
        print 'HELO error'
        exit()
    except smtplib.SMTPAuthenticationError:
        print 'Could not authenticate on smtp server, please check config file'
        exit()
    except smtplib.SMTPException:
        print 'Error while logging on smtp server'
        exit()

def sendmail(smtp, mail_to, message):
    try:
        smtp.sendmail(config.smtp_mail, mail_to, message)
    except smtplib.SMTPRecipientsRefused:
        print 'All email recipients were refused. Double-check the mail input'
        exit()
    except smtplib.SMTPHeloError:
        print 'HELO error'
        exit()
    except smtplib.SMTPSenderRefused:
        print 'The sender email was refused, verify your config parameters'
        exit()
    except smtplib.SMTPDataError:
        print 'An error happened while trying to send the email. Try again'
        exit()


mail_to = raw_input('E-mail: ')
subject = get_subject( raw_input('Subject: ') )
message = get_message(subject, mail_to)

smtp_mail(mail_to, message)

print 'Success sending mail to: '+mail_to+' -- '+str(datetime.datetime.now())
