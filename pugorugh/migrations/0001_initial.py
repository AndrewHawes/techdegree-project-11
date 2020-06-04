# Generated by Django 3.0.6 on 2020-06-04 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/dogs/')),
                ('breed', models.CharField(default='Unknown Breed', max_length=100)),
                ('_age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('u', 'Unknown')], max_length=1)),
                ('size', models.CharField(choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('xl', 'Extra Large'), ('u', 'Unknown')], max_length=2)),
                ('type', models.CharField(choices=[('m', 'Mammal'), ('r', 'Robot')], default='m', max_length=1)),
                ('birthdate', models.DateField(blank=True)),
                ('favorite_cat_food', models.CharField(blank=True, max_length=60, verbose_name='Favorite brand of cat food')),
                ('french_films', models.BooleanField(blank=True, default=False, verbose_name='Likes classy French films')),
                ('chicken_noises', models.BooleanField(blank=True, default=False, verbose_name='Unafraid to express its feelings with high-pitched chicken noises')),
                ('is_carl_sagan', models.BooleanField(blank=True, default=False)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(default='b,y,a,s', max_length=100)),
                ('gender', models.CharField(default='m,f', max_length=100)),
                ('size', models.CharField(default='s,m,l,xl', max_length=100)),
                ('type', models.CharField(default='m,r', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('l', 'Liked'), ('d', 'Disliked')], max_length=1, null=True)),
                ('hidden', models.BooleanField(default=False)),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pugorugh.Dog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
