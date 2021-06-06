from datetime import date
from django.db import models


class Slider(models.Model):
    img = models.ImageField()
    url = models.URLField(default='')


class News(models.Model):
    title = models.CharField(max_length=100, default='')
    text = models.TextField(default='')
    img = models.ImageField()
    time = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=100, default='')
    img = models.ImageField()

    def __str__(self):
        return self.name


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    name = models.CharField(max_length=100, default='')
    score_team_1 = models.PositiveIntegerField(default=0)
    score_team_2 = models.PositiveIntegerField(default=0)
    future_match = models.BooleanField(default=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    title = models.CharField(max_length=100, default='')
    logo = models.ImageField()
    url = models.URLField(default='')

    def __str__(self):
        return self.title


class Nationality(models.Model):
    country_name = models.CharField(max_length=100)
    logo = models.ImageField()

    def __str__(self):
        return self.country_name


class TypePlayer(models.Model):
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name


class Player(models.Model):
    CHOICES_TEAM = (
        ('M', 'Основа'),
        ('A', 'Академія'),
    )
    CHOICES_ROLES = (
        ('goalkeeper', 'Воротар'),
        ('defender', 'Захисник'),
        ('midfielder', 'Півзахисник'),
        ('attackers', 'Нападаючі')
    )
    first_name = models.CharField(max_length=100, default='noname')
    last_name = models.CharField(max_length=100, default='noname')
    number = models.PositiveIntegerField(default=0)
    nationality = models.ForeignKey(Nationality, null=True, on_delete=models.CASCADE, related_name='player')
    role_player = models.CharField(choices=CHOICES_ROLES, max_length=20, default='goalkeeper')
    decs = models.TextField(default='')
    date_of_birth = models.DateField(default=date.today)
    height = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)
    team = models.CharField(choices=CHOICES_TEAM, max_length=20)
    img = models.ImageField(default='gaga.jpeg')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
