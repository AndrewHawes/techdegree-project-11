from datetime import date

from dateutil.relativedelta import relativedelta as rd
from django.db import models

from pugorugh.utils.classutils import classproperty


class TextChoicesWrapper:
    class Choices(models.TextChoices):
        pass

    class Unknown(models.TextChoices):
        UNKNOWN = 'u', 'Unknown'

    @classproperty
    def ALL(cls):
        return ','.join(cls.Choices)

    @classproperty
    def choices(cls):
        return cls.Choices.choices

    @classproperty
    def wunk(cls):  # WUNK!! (w/ unknown)
        return cls.Choices.choices + cls.Unknown.choices


class Gender(TextChoicesWrapper):
    class Choices(models.TextChoices):
        MALE = 'm', 'Male'
        FEMALE = 'f', 'Female'


class Size(TextChoicesWrapper):
    class Choices(models.TextChoices):
        SMALL = 's', 'Small'
        MEDIUM = 'm', 'Medium'
        LARGE = 'l', 'Large'
        EXTRA_LARGE = 'xl', 'Extra Large'


def get_date_range(youngest, oldest):
    today = date.today()
    return today - rd(months=oldest), today - rd(months=youngest)


def get_date_ranges():
    return {
        'b': get_date_range(0, 10),
        'y': get_date_range(6, 18),
        'a': get_date_range(18, 72),
        's': get_date_range(72, 200)
    }


class Age(TextChoicesWrapper):
    today = date.today()
    _date_ranges = get_date_ranges()

    @classmethod
    def date_ranges(cls, age_classes):
        if cls.today != date.today():
            cls.today = date.today()
            cls._date_ranges = get_date_ranges()
        return [
            cls._date_ranges[age_class]
            for age_class in age_classes.split(',')
        ]

    class Choices(models.TextChoices):
        BABY = 'b', 'Baby'
        YOUNG = 'y', 'Young'
        ADULT = 'a', 'Adult'
        SENIOR = 's', 'Senior'


class Type(TextChoicesWrapper):
    class Choices(models.TextChoices):
        MAMMAL = 'm', 'Mammal'
        ROBOT = 'r', 'Robot'
