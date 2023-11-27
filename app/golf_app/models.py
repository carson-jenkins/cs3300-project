from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()  # Custom manager for your user model

    USERNAME_FIELD = 'username'  # Set to the field used for username

class Player(models.Model):
    name = models.CharField(max_length=200)
    handicap = models.IntegerField()
    contact_email = models.EmailField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    date = models.DateField()
    course_name = models.CharField(max_length=200)
    players = models.ManyToManyField('Player', through='PlayerGameScore', related_name='games')

    def __str__(self):
        return f"{self.course_name} on {self.date}"

class PlayerGameScore(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    scores = models.CharField(max_length=255, blank=True)  # Stores scores as a comma-separated string

    def __str__(self):
        return f"{self.player.name} - {self.game.course_name}"

    def set_scores(self, new_scores):
        # Ensure new_scores has 18 values (one for each hole)
        if len(new_scores) == 18:
            self.scores = ','.join(map(str, new_scores))
            self.save()

    def get_score(self, hole):
        scores_list = self.scores.split(',') if self.scores else [''] * 18
        if 1 <= hole <= 18:
            return scores_list[hole - 1]
        return ''

    def get_scores_as_list(self):
        scores_list = self.scores.split(',') if self.scores else [''] * 18
        return [int(score) if score.isdigit() else None for score in scores_list]
