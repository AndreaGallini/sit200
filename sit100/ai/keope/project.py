# Classe fittizia per simulare il modello Project
from ..keope.keopebank import KeopeBank
from django.db import models
from django.contrib.postgres.fields import JSONField


class Project(models.Model):
    name = models.CharField(max_length=100)
    keopebank = models.JSONField(null=True, blank=True)

    def update_keopebank(self, keopebank):
        # Metodo per serializzare e aggiornare il campo databank
        self. keopebank = keopebank.to_dict()
        self.save()

    def get_keopebank(self):
        # Metodo per deserializzare il campo keopebank
        return Keopebank.from_dict(self.keopebank) if self.keopebank else Keopebank()


'''



'''
