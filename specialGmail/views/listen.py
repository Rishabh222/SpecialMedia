__author__ = 'RishabhBhatia'
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.conf import settings


@api_view(['GET'])
def hello(request,text):
    f = open(settings.SPEECH_TO_TEXT_FILE_NAME, 'w')
    f.write(text)
    print text
    return HttpResponse(text)

