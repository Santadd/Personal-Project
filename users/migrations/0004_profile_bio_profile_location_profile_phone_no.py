# Generated by Django 4.0.6 on 2022-07-26 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='N/A'),
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(default='N/A', max_length=250),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_no',
            field=models.CharField(default='N/A', max_length=120),
        ),
    ]
