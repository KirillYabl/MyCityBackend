# Generated by Django 4.1.6 on 2023-04-07 16:08

from django.db import migrations

import user_app.managers


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', user_app.managers.UserManager()),
            ],
        ),
    ]
