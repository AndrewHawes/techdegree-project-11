from datetime import date

from django.db import models
from django.db.models import Q


class DogManager(models.Manager):
    baby = 0, 10
    young = 10, 18
    adult = 18, 72
    senior = 72, 180


    def by_age(self, preferred_ages):
        queries = [Q(**{
            'birthdate__range': (age_range.start, age_range.end)
            for age_range in preferred_ages
        })]
        qs = Q()
        for query in queries:
            qs |= query


class UserDogQuerySet(models.QuerySet):
    def liked(self):
        return self.filter(status='l')

    def disliked(self):
        return self.filter(status='d')


class UserDogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
