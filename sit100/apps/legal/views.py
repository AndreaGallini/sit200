from django.shortcuts import render
import time
from django.conf import settings

APP_NAME = settings.APP_NAME
# Create your views here.


def cookies(request):
    context = {'time': time, 'APP_NAME': APP_NAME}
    return render(request, 'legal/cookies.html', context)


def privacy(request):
    context = {'time': time, 'APP_NAME': APP_NAME}
    return render(request, 'legal/privacy.html', context)


def terms(request):
    context = {'time': time, 'APP_NAME': APP_NAME}
    return render(request, 'legal/terms_conditions.html', context)


def disclaimer(request):
    context = {'time': time, 'APP_NAME': APP_NAME}
    return render(request, 'legal/disclaimer.html', context)
