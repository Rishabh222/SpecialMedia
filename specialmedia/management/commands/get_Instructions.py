__author__ = 'RishabhBhatia'
# encoding=utf8
from django.core.management import BaseCommand
import sched, time
from django.conf import settings
import os
import re
from specialGmail.views.gmail_functions import authenticateUser, unreadMessages, CreateMessage, SendMessage

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

def start_reading(sc, last_read_time=0):
    try:

        f = open(settings.SPEECH_TO_TEXT_FILE_NAME,'r')
        statbuf = os.stat(settings.SPEECH_TO_TEXT_FILE_NAME)
        if statbuf.st_mtime > last_read_time:
            lines = f.readlines()
            last_read_time = statbuf.st_mtime
            x=lines[0].split()
            print x
            if "mails" in x or "mail" in x:
                service = authenticateUser()
                if "unread" in x:
                    unreadMessages(service,'me')
                elif "send" in x:
                    to_mail_ids = re.findall(r'[\w\.-]+@[\w\.-]+',lines[0])
                    f = open(settings.TEXT_TO_SPEECH_FILE_NAME,'w')
                    f.write("what message text u want to send")
                    time.sleep(10)
                    f = open(settings.SPEECH_TO_TEXT_FILE_NAME,'r')
                    lines = f.readlines()
                    for x in to_mail_ids:
                        message=CreateMessage('me',x,""," ".join(lines))
                        SendMessage(service,'me',message)
                    print "mail sent"
                    f = open(settings.TEXT_TO_SPEECH_FILE_NAME,'w')
                    f.write("Mail sent to "+" ".join(to_mail_ids))
            f.close()

        sc.enter(read_settimgs.get('BATCH_TIME_INTERVAL'), 1, start_reading, (sc,last_read_time,))
    except Exception as e:
        on_read_run_failed(e)
        sc.enter(read_settimgs.get('BATCH_TIME_INTERVAL'), 1, start_reading, (sc,last_read_time,))

def on_read_run_failed(message):
    # log it
    pass