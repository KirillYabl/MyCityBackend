# Generated by Django 4.1.6 on 2023-03-28 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
        ('quest_app', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='categories', to='user_app.team', verbose_name='участвующие команды'),
        ),
    ]
