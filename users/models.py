from django.db import models

# Create your models here.

class UpUser(models.Model):

    class Meta():
        db_table = 'upuser'

    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200, null=False)
