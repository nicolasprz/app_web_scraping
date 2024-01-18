from django.db import models


# Create your models here.
class UserInput(models.Model):
    text_input = models.TextField()
    output = models.TextField()
