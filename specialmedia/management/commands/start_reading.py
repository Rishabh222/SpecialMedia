__author__ = 'RishabhBhatia'
# encoding=utf8
from django.core.management import BaseCommand
import sched, time
from django.conf import settings
import os
import subprocess
# import pyttsx
# from Foundation import *
# engine = pyttsx.init()
# engine.setProperty('rate', 70)

# voices = engine.getProperty('voices')
read_settings = settings.READ_INSTRUCTION_SETTINGS

class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        self.on_command_started()
        s = sched.scheduler(time.time, time.sleep)
        s.enter(read_settings.get('BATCH_TIME_INTERVAL'), 1, text_to_speech, (s,))
        s.run()
        self.on_command_stopped()

    def on_command_started(self):
        # log it
        pass

    def on_command_stopped(self):
        # log it
        pass

def text_to_speech(sc, last_read_time=0):
    try:

        f = open(settings.TEXT_TO_SPEECH_FILE_NAME,'r')
        statbuf = os.stat(settings.TEXT_TO_SPEECH_FILE_NAME)
        if statbuf.st_mtime > last_read_time:
            lines = f.readlines()
            last_read_time = statbuf.st_mtime
            # print lines
            #logic for reading from file
            for x in lines:
                subprocess.call('say ' + x ,shell=True)

            # for voice in voices:
            #     print "Using voice:", repr(voice)
            #     engine.setProperty('voice', voice.id)
            #     engine.say("Hi there, how's you ?")
            # engine.runAndWait()

            f.close()

        sc.enter(read_settings.get('BATCH_TIME_INTERVAL'), 1, text_to_speech, (sc, last_read_time,))
    except Exception as e:
        sc.enter(read_settings.get('BATCH_TIME_INTERVAL'), 1, text_to_speech, (sc, last_read_time,))
