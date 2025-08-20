from django.shortcuts import render
import time
from django.conf import settings

APP_NAME = settings.APP_NAME



def docs(request):
    context = {'time': time, 'version': settings.VERSION, 'APP_NAME': APP_NAME}
    return render(request, 'documentation/documentazione.html', context)
