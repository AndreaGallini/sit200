from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordForm
from django.utils import timezone
from datetime import timedelta
# Assumo che FailedLoginAttempt sia definito in models.py nella stessa app
from .models import FailedLoginAttempt


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.request = request

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email:
            # Controlla se l'utente esiste
            try:
                user = User.objects.get(email=email)

                # Modifica questa parte: invece di contare i tentativi, verifica se c'è un record bloccato
                attempts = FailedLoginAttempt.objects.filter(user=user).first()
                if attempts and attempts.is_locked():
                    remaining_time = attempts.get_remaining_lockout_time()
                    raise forms.ValidationError(
                        f"Account bloccato per troppi tentativi falliti. "
                        f"Riprova tra {remaining_time} minuti."
                    )

                # Procedi con l'autenticazione
                if password:
                    self.user_cache = authenticate(
                        username=email, password=password)
                    if self.user_cache is None:
                        # Get IP address from request
                        if self.request:
                            ip_address = self.request.META.get(
                                'REMOTE_ADDR', '0.0.0.0')
                        else:
                            ip_address = '0.0.0.0'  # Fallback value if no request available

                        # Invece di creare un nuovo record ogni volta, cerca un record esistente o creane uno nuovo
                        try:
                            # Cerca un record esistente per lo stesso utente e IP
                            attempt = FailedLoginAttempt.objects.get(
                                user=user, ip_address=ip_address)
                            # Incrementa il contatore (questo metodo imposta anche locked_until se necessario)
                            attempt.increment_attempts()
                        except FailedLoginAttempt.DoesNotExist:
                            # Se non esiste, crea un nuovo record
                            attempt = FailedLoginAttempt.objects.create(
                                user=user,
                                ip_address=ip_address
                            )

                        # Verifica se l'account è ora bloccato
                        if attempt.is_locked():
                            raise forms.ValidationError(
                                "Account bloccato per troppi tentativi falliti. "
                                f"Riprova tra {attempt.get_remaining_lockout_time()} minuti."
                            )
                        else:
                            raise forms.ValidationError(
                                self.error_messages['invalid_login'],
                                code='invalid_login',
                                params={
                                    'username': self.username_field.verbose_name},
                            )
                    else:
                        # Login riuscito, elimina i tentativi falliti
                        FailedLoginAttempt.objects.filter(user=user).delete()

            except User.DoesNotExist:
                # Non rivelare che l'utente non esiste per motivi di sicurezza
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

        return self.cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendi i campi password non richiesti
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # Opzionale: aggiungi un help text per chiarire il comportamento
        self.fields['password1'].help_text = "La password verrà generata automaticamente e inviata via email."
        self.fields['password2'].help_text = "Non necessario, la password verrà generata automaticamente."

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Questa email è già registrata.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username

    # Override della validazione password per permettere password vuote
    def clean_password2(self):
        # Non validiamo la corrispondenza delle password perché verranno ignorate
        return self.cleaned_data.get('password2', '')


class FirstPasswordSetForm(SetPasswordForm):
    """
    Form che permette di impostare la password per la prima volta.
    Richiede la vecchia password, una nuova e la conferma.
    """
    old_password = forms.CharField(
        label="Vecchia password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Vecchia password'})
    )

    new_password1 = forms.CharField(
        label="Nuova password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Nuova password'})
    )

    new_password2 = forms.CharField(
        label="Conferma password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Conferma nuova password'})
    )

    def clean_old_password(self):
        """
        Verifica che la vecchia password sia corretta.
        """
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                "La vecchia password non è corretta. Riprova.",
                code='password_incorrect',
            )
        return old_password
