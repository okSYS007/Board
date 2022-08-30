# Generated by Django 4.1 on 2022-08-30 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.TextField(blank=True),
        ),
    ]
