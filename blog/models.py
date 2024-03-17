from django.db import models


# Create your models here.
class UserInput(models.Model):
    text_input = models.TextField()
    output = models.TextField()


class Option(models.Model):
    value = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
