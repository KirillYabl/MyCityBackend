# Generated by Django 4.1.6 on 2023-03-09 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_member_team_teammembership_member_team'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
        migrations.AlterUniqueTogether(
            name='teammembership',
            unique_together={('team', 'member', 'member_number')},
        ),
    ]