from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Exercises(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    points = models.IntegerField(default=0)
    exercises_time = models.CharField(max_length=8, default=1)
    detalis= models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.name}'

class DayName(models.Model):
    name = models.CharField(max_length=32)
    order = models.SmallIntegerField(unique=True)

    def __str__(self):
        return f'{self.name}'


class Plan(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    exercises = models.ManyToManyField(Exercises, through='ExercisesPlan')

    def __str__(self):
        return f'{self.name}'


class ExercisesPlan(models.Model):
    workout_name = models.CharField(max_length=64)
    exercises = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)

    
    def __str__(self):
        return f'Plan for: {self.plan}'


class Page(models.Model):
    title = models.CharField(max_length=126)
    description = models.TextField()
    slug = models.SlugField(null=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'slug': self.slug})

