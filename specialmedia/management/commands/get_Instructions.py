__author__ = 'RishabhBhatia'
# encoding=utf8
from django.core.management import BaseCommand
import sched, time
from django.conf import settings
import os
import re
from specialGmail.views.gmail_functions import authenticateUser, unreadMessages, CreateMessage, SendMessage, \
    GetSubjects, \
    DeleteMessage
import difflib

read_settimgs = settings.READ_INSTRUCTION_SETTINGS


class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        self.on_command_started()
        s = sched.scheduler(time.time, time.sleep)
        s.enter(read_settimgs.get('BATCH_TIME_INTERVAL'), 1, start_reading, (s,))
        s.run()
        self.on_command_stopped()

    def on_command_started(self):
        # log it
        pass

    def on_command_stopped(self):
        # log it
        pass


def start_reading(sc, last_read_time=0, subj_id_mapping={}):
    try:
        print subj_id_mapping,1
        f = open(settings.SPEECH_TO_TEXT_FILE_NAME, 'r')
        statbuf = os.stat(settings.SPEECH_TO_TEXT_FILE_NAME)
        if statbuf.st_mtime > last_read_time:
            lines = f.readlines()
            last_read_time = statbuf.st_mtime
            x = lines[0].split('+')
            print x
            if "mails" in x or "mail" in x:
                service = authenticateUser()
                if "unread" in x:
                    unreadMessages(service, 'me')
                elif "send" in x:
                    to_mail_ids = re.findall(r'[\w\.-]+@[\w\.-]+', lines[0])
                    f = open(settings.TEXT_TO_SPEECH_FILE_NAME, 'w')
                    f.write("what message text u want to send ?")
                    time.sleep(10)
                    f = open(settings.SPEECH_TO_TEXT_FILE_NAME, 'r')
                    lines = f.readlines()
                    for x in to_mail_ids:
                        message = CreateMessage('me', x, "", " ".join(lines))
                        SendMessage(service, 'me', message)
                    print "mail sent"
                    f = open(settings.TEXT_TO_SPEECH_FILE_NAME, 'w')
                    f.write("Mail sent to " + " ".join(to_mail_ids))
                elif "delete" in x and "subject" not in x:
                    del_mail_ids = re.findall(r'[\w\.-]+@[\w\.-]+', lines[0])
                    f = open(settings.TEXT_TO_SPEECH_FILE_NAME, 'w')
                    f.write("which message u want to delete ? Here are few options :")
                    del_ids = ""
                    for ids in del_mail_ids:
                        del_ids += ids + " "
                    subj_id_mapping = GetSubjects(service, 'me', del_ids)
                    print subj_id_mapping
                    # time.sleep(10)
                    #
                    # while last_read_time >= statbuf.st_mtime:
                    #     print last_read_time
                    #     print statbuf.st_mtime
                    #     statbuf = os.stat(settings.SPEECH_TO_TEXT_FILE_NAME)
                    # print "hello"
                    # last_read_time = statbuf.st_mtime
                elif "delete" in x and "subject" in x:
                    print "hello"
                    f = open(settings.SPEECH_TO_TEXT_FILE_NAME, 'r')
                    lines = f.readlines()
                    print lines
                    max = 0.0
                    del_id = ''
                    print subj_id_mapping
                    for x in subj_id_mapping:
                        if difflib.SequenceMatcher(None, x.split(' '), lines[0].split('+')) > max:
                            max = difflib.SequenceMatcher(None, subj_id_mapping[x].split(' '), lines[0].split('+'))
                            del_id = x

                    if del_id != '':
                        DeleteMessage(service, 'me', del_id)

            f.close()

        sc.enter(read_settimgs.get('BATCH_TIME_INTERVAL'), 1, start_reading, (sc, last_read_time, subj_id_mapping,))
    except Exception as e:
        on_read_run_failed(e)
        sc.enter(read_settimgs.get('BATCH_TIME_INTERVAL'), 1, start_reading, (sc, last_read_time, subj_id_mapping,))


def on_read_run_failed(message):
    # log it
    pass
