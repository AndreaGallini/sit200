from django.db import models
from django.conf import settings
from django.utils import timezone
import json


# Create your models here.
class Counter(models.Model):

    name = models.CharField(max_length=50, unique=True)
    value = models.PositiveIntegerField(default=1000)
    time_at = models.DateTimeField(default=timezone.now)


class Project(models.Model):

    id = models.AutoField(primary_key=True)
    project_code = models.PositiveIntegerField(unique=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    input_data = models.TextField(default='')
    pvgis_data = models.TextField(default='')
    word_file = models.TextField(default='')
    pdf_file = models.TextField(default='')
    status = models.SmallIntegerField(default=1)
    keopebank = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_files/user_<id>/<filename>
    return f'user_files/user_{instance.user.id}/{filename}'


class Designer(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    designer_data = models.JSONField(default=dict)
    logo = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.designer_data.get('designer_name', 'Unnamed Designer')

    def get_designer_data(self):
        """Restituisce i dati del designer come dizionario."""
        try:
            return json.loads(self.designer_data)
        except json.JSONDecodeError:
            return {}
