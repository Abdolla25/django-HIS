from enum import unique
from unicodedata import name
from django.db import models


# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    details = models.TextField()    
    location = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField()
    age = models.IntegerField()
    position_in_field = models.CharField(max_length=200, choices=(('goal', 'Goalkeeper'),('def', 'Defender'),('mid', 'Midfielder'),('atk', 'Attacker')))
    is_captain = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name

class GameScore(models.Model):
    first_team = models.CharField(max_length=200)
    second_team = models.CharField(max_length=200)
    first_team_score = models.IntegerField(default=0)
    second_team_score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return ('{} : {}  |  {} : {}'.format(self.first_team, self.first_team_score, self.second_team, self.second_team_score))