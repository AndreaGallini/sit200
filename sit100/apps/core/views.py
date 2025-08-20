import json
import os
import time
from dotenv import load_dotenv
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.core.mail import EmailMultiAlternatives
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from user_agents import parse
from .forms import CustomAuthenticationForm, FirstPasswordSetForm
from .models import UserAccessLog
from django.conf import settings

APP_NAME = settings.APP_NAME


load_dotenv()


def home(request):
    return render(request, 'home.html')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class FirstPasswordSetView(PasswordResetConfirmView):
    template_name = 'registration/set_first_password.html'
    form_class = FirstPasswordSetForm
    success_url = '/login/'  # Redirect all'accesso dopo il cambio password

    def dispatch(self, *args, **kwargs):
        # Prima eseguiamo il dispatch standard di Django che verifica la validità del token
        response = super().dispatch(*args, **kwargs)
        # Se siamo in POST (invio form), Django gestirà tutto
        if self.request.method == 'POST':
            return response

        # Verifichiamo se siamo in GET e se il token è valido ma l'utente ha già cambiato password
        if self.request.method == 'GET' and hasattr(self, 'user'):
            # Controlliamo se l'utente esiste e ha una password definitiva
            # Possiamo verificare se l'utente ha last_login diverso da None,
            # questo indica che l'utente ha già effettuato almeno un login
            # (quindi ha già impostato una password definitiva)
            if self.user.last_login is not None:
                return render(self.request, 'registration/password_already_set.html', {
                    'message': 'Hai già impostato la tua password definitiva. Utilizza la pagina di login.'
                })

        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        # Imposta manualmente il valore di last_login per evitare che l'utente venga ridiretto
        # nuovamente alla pagina di impostazione password
        if hasattr(self, 'user'):
            self.user.last_login = timezone.now()
            self.user.save()
        return response


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()

        # Recupera informazioni sull'User-Agent
        user_agent_string = self.request.META['HTTP_USER_AGENT']
        user_agent = parse(user_agent_string)

        # Determina il tipo di dispositivo
        if user_agent.is_mobile:
            device_type = "Mobile"
        elif user_agent.is_tablet:
            device_type = "Tablet"
        elif user_agent.is_pc:
            device_type = "PC"
        else:
            device_type = "Other"

        os_family = user_agent.os.family
        browser_family = user_agent.browser.family
        browser_version = user_agent.browser.version_string

        # Costruisce una stringa rappresentativa del dispositivo
        if user_agent.is_pc and "Mac" in os_family:
            device_info = f" Dispositivo: Mac - Browser: {browser_family} "
        else:
            device_info = f"Dispositivo:{device_type} - Sistema operativo:{os_family} - Browser:{browser_family} "

        ip = get_client_ip(self.request)
        # Puoi usare un servizio di geolocalizzazione per determinare la posizione
        location = "Unknown"

        # Crea un log di accesso
        UserAccessLog.objects.create(
            user=user, device=device_info, location=location)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aggiungi l'ora corrente al contesto
        context['time'] = time
        return context


def logout_view(request):
    context = {'time': time, 'APP_NAME': APP_NAME}
    logout(request)
    return render(request, 'logout_success.html', context)


def access_logs_view(request):
    logs = list(request.user.access_logs.all().values(
        'device', 'location', 'access_time'))
    context = {
        'logs': json.dumps(logs, cls=DjangoJSONEncoder),
        'APP_NAME': APP_NAME,
        'time': time
    }
    return render(request, 'user_profile/access_log.html', context)


def send_reset_password_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Reset password su kWh91"
                from_email = settings.DEFAULT_FROM_EMAIL
                to = [user.email]

                # Dati dinamici
                context = {
                    "user_name": user.get_username(),
                    "email": user.email,
                    'domain': request.get_host(),
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': os.getenv('PROTOCOL'),
                }

                # Caricamento e rendering dei template con dati dinamici
                html_content = render_to_string(
                    'emails/reset_email.html', context)
                text_content = strip_tags(render_to_string(
                    'emails/reset_email.html', context))

                msg = EmailMultiAlternatives(
                    subject, text_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

        return redirect("password_reset_done")
    return render(request, 'registration/password_reset_form.html')
