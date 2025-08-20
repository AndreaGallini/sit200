from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserAccessLog(models.Model):
    class Meta:
        app_label = 'core'
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='access_logs')
    device = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    access_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.access_time}'

# Modello per gestire i tentativi di login falliti


class FailedLoginAttempt(models.Model):
    class Meta:
        app_label = 'core'

    # Per tentativi associati a un utente esistente
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='failed_logins', null=True, blank=True)

    # Per tentativi su email non registrate
    email = models.EmailField(null=True, blank=True)

    # Indirizzo IP per bloccare tentativi da uno stesso IP
    ip_address = models.GenericIPAddressField()

    # Numero di tentativi falliti
    attempts_count = models.PositiveIntegerField(default=1)

    # Quando l'utente è stato bloccato
    locked_until = models.DateTimeField(null=True, blank=True)

    # Timestamp dell'ultimo tentativo fallito
    last_attempt = models.DateTimeField(auto_now=True)

    def is_locked(self):
        if self.locked_until and timezone.now() < self.locked_until:
            return True
        return False

    def get_remaining_lockout_time(self):
        if not self.is_locked():
            return 0

        time_diff = self.locked_until - timezone.now()
        return int(time_diff.total_seconds() // 60)  # Minuti rimanenti

    def increment_attempts(self):
        self.attempts_count += 1

        # Blocca l'account dopo 5 tentativi falliti
        if self.attempts_count >= 5:
            # Blocca per 30 minuti
            self.locked_until = timezone.now() + timezone.timedelta(minutes=30)

        self.save()

    def reset_attempts(self):
        self.attempts_count = 0
        self.locked_until = None
        self.save()
