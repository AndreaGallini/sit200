from django.shortcuts import render
import time
from django.conf import settings

APP_NAME = settings.APP_NAME
# Create your views here.


def home(request):
    context = {'time': time, 'APP_NAME': APP_NAME}
    return render(request, 'frontend/homepage.html', context)
