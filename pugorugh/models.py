from datetime import date
import os

from dateutil.relativedelta import relativedelta as rd

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .choices import Age, Gender, Size, Type


class Dog(models.Model):
    added_by = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/dogs/', blank=True, null=True)
    breed = models.CharField(max_length=100, default='Unknown Breed')
    _age = models.PositiveIntegerField()  # in months
    gender = models.CharField(max_length=1, choices=Gender.wunk)
    size = models.CharField(max_length=2, choices=Size.wunk)
    type = models.CharField(max_length=1, choices=Type.choices, default=Type.Choices.MAMMAL)
    birthdate = models.DateField(blank=True)  # calculated from _age

    favorite_cat_food = models.CharField(
        max_length=60,
        blank=True,
        verbose_name='Favorite brand of cat food'
    )
    french_films = models.BooleanField(
        blank=True,
        default=False,
        verbose_name='Likes classy French films'
    )
    chicken_noises = models.BooleanField(
        blank=True,
        default=False,
        verbose_name='Unafraid to express its feelings with high-pitched chicken noises'
    )
    is_carl_sagan = models.BooleanField(blank=True, default=False)

    @property
    def image_filename(self):
        return os.path.basename(self.image.name)

    @property
    def age(self):
        elapsed = rd(date.today(), self.birthdate)
        return elapsed.years * 12 + elapsed.months

    @age.setter
    def age(self, value):
        # Set age and approximate birth date
        self._age = value
        self.birthdate = date.today() - rd(months=self._age)


@receiver(post_delete, sender=Dog)
def image_delete(sender, instance, **kwargs):
    instance.image.delete(False)


class UserDog(models.Model):
    class Status(models.TextChoices):
        LIKED = 'l', 'Liked'
        DISLIKED = 'd', 'Disliked'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=Status.choices, null=True)
    hidden = models.BooleanField(default=False)


class UserPref(models.Model):

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    age = models.CharField(max_length=100, default=Age.ALL)
    gender = models.CharField(max_length=100, default=Gender.ALL)
    size = models.CharField(max_length=100, default=Size.ALL)
    type = models.CharField(max_length=100, default=Type.ALL)

    def get_preferred_ages(self):
        dogs = Dog.objects.all()

        if self.age != Age.ALL:
            queries = [
                Q(**{'birthdate__range': date_range})
                for date_range in Age.date_ranges(self.age)
            ]
            qs = Q()
            for query in queries:
                qs = qs | query
            dogs = dogs.filter(qs)
        return dogs

    def get_preferred_dogs(self):
        # Doesn't apply filter if all options are selected.
        dogs = Dog.objects.all()

        if len(self.age) < len(Age.ALL):
            dogs = self.get_preferred_ages()

        if len(self.gender) < len(Gender.ALL):
            dogs = dogs.filter(gender__in=self.gender)

        if len(self.size) < len(Size.ALL):
            dogs = dogs.filter(size__in=self.size.split(','))

        if len(self.type) < len(Type.ALL):
            dogs = dogs.filter(type__in=self.type)

        return dogs
