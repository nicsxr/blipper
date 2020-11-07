# Generated by Django 3.1.1 on 2020-11-06 17:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20201106_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='followers',
            field=models.ManyToManyField(related_name='u_followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='account',
            name='following',
            field=models.ManyToManyField(related_name='u_following', to=settings.AUTH_USER_MODEL),
        ),
    ]