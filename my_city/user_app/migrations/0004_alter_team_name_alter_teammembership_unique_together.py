# Generated by Django 4.1.6 on 2023-03-09 20:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(message='в названии команды допускаются русские и английские буквы, цифры и пробелы если название содержит несколько слов', regex='^[ёЁа-яА-Я\\p{P}\\w]+( [ёЁа-яА-Я\\p{P}\\w]+)*$')], verbose_name='название команды'),
        ),
        migrations.AlterUniqueTogether(
            name='teammembership',
            unique_together={('team', 'member', 'member_number'), ('team', 'member')},
        ),
    ]
