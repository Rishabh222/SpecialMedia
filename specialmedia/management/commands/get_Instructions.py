__author__ = 'RishabhBhatia'
# encoding=utf8
from django.core.management import BaseCommand
import sched, time
from django.conf import settings
import os
from specialGmail.views.gmail_functions import authenticateUser, unreadMessages

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
            if "mails" in x:
                service = authenticateUser()
                if "unread" in x:
                    unreadMessages(service,'me')
                elif "send" in x:
                    pass

            f.close()

        sc.enter(read_settimgs.get('BATCH_TIME_INTERVAL'), 1, start_reading, (sc,last_read_time,))
    except Exception as e:
        on_read_run_failed(e)
        sc.enter(read_settimgs.get('BATCH_TIME_INTERVAL'), 1, start_reading, (sc,last_read_time,))

def on_read_run_failed(message):
    # log it
    pass