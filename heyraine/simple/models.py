from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


class room(models.Model):
    roomID = models.CharField(max_length=200)
    personID = models.CharField(max_length=200)
