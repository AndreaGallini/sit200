"""
    Si occupa di mandare l'email di benvenuto
    """
import os
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from dotenv import load_dotenv


load_dotenv()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Si occupa di mandare l'email di benvenuto
    """
    if created:
        # Controlla se l'utente è un superuser
        if not instance.is_superuser and instance.username != 'testuser':
            # Genera una password casuale solo per utenti non superuser
            password = get_random_string(8)
            instance.set_password(password)
            instance.save()

            # Prepara il messaggio email usando un template HTML
            subject = 'Benvenuto in kWh91'
            from_email = os.getenv('DEFAULT_FROM_EMAIL')

            # Contesto per il template
            context = {
                'user': instance,
                'password': password,
                'email': instance.email,
                'domain': os.getenv('DOMAIN'),
                'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                'token': default_token_generator.make_token(instance),
                'protocol': os.getenv('PROTOCOL')
            }

            # Renderizza il template HTML
            html_content = render_to_string(
                'emails/welcome_email.html', context)
            text_content = f'Ciao {instance.email}, sei stato registrato con successo. La tua password è: {password}'

            # Crea il messaggio email
            msg = EmailMultiAlternatives(
                subject,
                text_content,  # Versione testuale
                from_email,
                [instance.email]
            )

            # Aggiungi la parte HTML
            msg.attach_alternative(html_content, "text/html")
            # Invia l'email
            msg.send()
