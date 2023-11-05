from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Player(models.Model):
    name = models.CharField(max_length=100)
    handicap = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Game(models.Model):

    date_played = models.DateField(null=True, blank=True)
    course_name = models.CharField(max_length=100, null=True, blank=True)
    players = models.ManyToManyField(Player)

    def __str__(self):
        return f"{self.course_name} on {self.date_played}"