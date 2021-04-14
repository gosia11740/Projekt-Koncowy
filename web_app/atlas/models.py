from django.db import models

class Hello(models.Model):
    name = models.CharField(max_length=64)