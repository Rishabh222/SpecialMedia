# -*- coding: utf-8 -*-
# encoding=utf8

# from __future__ import print_function

from logging import exception

__author__ = 'RishabhBhatia'

import httplib2
import os
import base64
import email
import mimetypes
import oauth2client
from apiclient import discovery
from django.conf import settings
from oauth2client import client
from oauth2client import tools
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser])
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/ https://www.googleapis.com/auth/gmail.compose https://www.googleapis.com/auth/gmail.labels https://www.googleapis.com/auth/gmail.insert https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = '/Users/rcipher222/final-chutiyapa/SpecialMedia/client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def ListMessagesMatchingQuery(service, user_id, query=''):
    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError, error:
        print(error)


def ListMessagesWithLabels(service, user_id, label_ids=[]):
    try:
        response = service.users().messages().list(userId=user_id,
                                                       labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,
                                                       labelIds=label_ids,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError, error:
        print (error)


def GetMessage(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        # print (message['snippet'])

        return message
    except errors.HttpError, error:
        print(error)


def GetMimeMessage(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='raw').execute()

        print (message['snippet'])

        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

        mime_msg = email.message_from_string(msg_str)

        return mime_msg
    except errors.HttpError, error:
        print (error)


def authenticateUser():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    print "authenticated"
    return service


def unreadMessages(service, user_id):
    list_unread_messages_ids = ListMessagesMatchingQuery(service, user_id, 'label:unread')
    messages = {}
    f = open(settings.TEXT_TO_SPEECH_FILE_NAME, 'w')
    for list_unread_messages_id in list_unread_messages_ids:
        messages[list_unread_messages_id['id']] = GetMessage(service, user_id, list_unread_messages_id['id'])

    writeGivenMessageIds(messages)

def readTopUnreadMails(service, maxResults):
    response = service.users().messages().list(userId='me',
                                                   q='label:unread',maxResults=maxResults).execute()
    list_top_unread_messages_ids = []
    if 'messages' in response:
        list_top_unread_messages_ids.extend(response['messages'])
    messages = {}
    for list_messages_id in list_top_unread_messages_ids:
        messages[list_messages_id['id']] = GetMessage(service, 'me', list_messages_id['id'])

    writeGivenMessageIds(messages)
def readTopMails(service, maxResults):
    response = service.users().messages().list(userId='me', maxResults=maxResults).execute()
    list_top_read_messages_ids = []
    if 'messages' in response:
        list_top_read_messages_ids.extend(response['messages'])
    messages = {}

    for list_messages_id in list_top_read_messages_ids:
        messages[list_messages_id['id']] = GetMessage(service, 'me', list_messages_id['id'])

    writeGivenMessageIds(messages)

def GetSubjects(service, user_id, query):
    list_messages_ids = ListMessagesMatchingQuery(service, user_id, 'label:unread ' + query)

    messages = {}
    all_subjects = ""
    subj_id_mapping = {}
    for list_messages_id in list_messages_ids:
        messages[list_messages_id['id']] = GetMessage(service, user_id, list_messages_id['id'])
        subject = ""

        # print messages[list_messages_id['id']]['payload']['headers'][16]
        if messages[list_messages_id['id']]['payload']['headers'][16][u'name'] == 'Subject':
            subject = messages[list_messages_id['id']]['payload']['headers'][16][u'value']

            if len(subject) == 0:
                s = messages[list_messages_id['id']]['snippet'].encode('ascii', 'ignore').decode(
                    'ascii')
                all_subjects += "No Subject " + messages[list_messages_id['id']]['snippet'].encode('ascii',
                                                                                                   'ignore').decode(
                    'ascii') + '\n'

            else:
                all_subjects += "" + subject + '\n'

        else:
            for headers in messages[list_messages_id['id']]['payload']['headers']:

                if headers[u'name'] == 'Subject':
                    subject = headers[u'value']
                    if len(subject) == 0:
                        all_subjects += "No Subject ... content is " + messages[list_messages_id['id']][
                            'snippet'].encode('ascii',
                                              'ignore').decode(
                            'ascii') + '\n'
                    else:
                        all_subjects += " " + subject + '\n'
                    break
        if len(subject) == 0:
            subj_id_mapping[list_messages_id['id']] = "No Subject"
        else:
            subj_id_mapping[list_messages_id['id']] = subject

    print all_subjects
    f = open(settings.TEXT_TO_SPEECH_FILE_NAME, 'w')
    f.write(all_subjects)
    for x in subj_id_mapping:
        print subj_id_mapping[x]
    return subj_id_mapping
    # print messages

    # for msg in messages:
    #     print {"=======>\n\n", messages[msg]['payload']['headers'][16], messages[msg]['payload']['headers'][17],
    #            messages[msg]['payload']['headers'][15], "\n\n<======"}
    #
    #     try:
    #         # s = messages[msg]['snippet'].encode('ascii', 'ignore').decode('ascii')
    #
    #         if messages[msg]['payload']['headers'][16]['name'] is "subject":
    #             subject =  messages[msg]['payload']['headers'][16]['value']
    #             f.write( subject + '\n')
    #         else:
    #             for headers in messages[msg]['payload']['headers']:
    #                 if headers['name'] is 'from':
    #                     subject = messages[msg]['payload']['headers'][16]['value']
    #                     f.write(" " + subject + '\n')
    #                     break
    #         if messages[msg]['payload']['headers'][15]['name'] is "Message-ID":
    #             msg_id = messages[msg]['payload']['headers'][15]['value']
    #         else:
    #             for headers in messages[msg]['payload']['headers']:
    #                 if headers['name'] is 'Message-ID':
    #                     msg_id = headers['value']
    #
    #         subj_id_mapping = {"msg_id":msg_id,"subject":subject}
    #     except Exception as e:
    #         print(e)


def SendMessage(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print 'Message Id: %s' % message['id']
        return message
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def CreateMessage(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def CreateMessageWithAttachment(
        sender, to, subject, message_text, file_dir, filename):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    path = os.path.join(file_dir, filename)
    content_type, encoding = mimetypes.guess_type(path)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(path, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(path, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(path, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(path, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def DeleteMessage(service, user_id, msg_id):
    try:
        service.users().messages().delete(userId=user_id, id=msg_id).execute()
        print 'Message with id: %s deleted successfully.' % msg_id
    except errors.HttpError, error:
        print 'An error occurred: %s' % error

def writeGivenMessageIds(messages={}):
    write_msg=""
    for msg in messages:
        try:
            # print("writing",messages[msg]['snippet'],"from:",messages[msg]['payload']['headers'][3]['value'])
            s = messages[msg]['snippet'].encode('ascii', 'ignore').decode('ascii')
            frm = ""

            if messages[msg]['payload']['headers'][17][u'name'] == 'From':
                frm = messages[msg]['payload']['headers'][17][u'value']
                write_msg += "mail from " + frm + " is " + s + '\n'
                # f.write("mail from " + frm + " is " + s + '\n')
            else:
                for headers in messages[msg]['payload']['headers']:
                    if headers['name'] == 'From':
                        frm = headers[u'value']
                        write_msg += "mail from " + frm + " is " + s + '\n'
                        # f.write("mail from " + frm + " is " + s + '\n')
                        break

            if frm == "":
                write_msg += "mail from " + messages[msg]['payload']['headers'][3]['value'][1:-1] + " is " + s + '\n'
                # f.write("mail from " + messages[msg]['payload']['headers'][3]['value'][1:-1] + " is " + s + '\n')

        except Exception as e:
            print(e)

    f = open(settings.TEXT_TO_SPEECH_FILE_NAME, 'w')
    f.write(write_msg)
    f.close()
