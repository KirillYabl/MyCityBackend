# Generated by Django 4.1.6 on 2023-03-29 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest_app', '0003_alter_category_teams'),
    ]

    operations = [
        migrations.AddField(
            model_name='quest',
            name='address',
            field=models.CharField(default='migration_address', max_length=256, verbose_name='адрес'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quest',
            name='banner',
            field=models.ImageField(default='quests/default_picture.png', upload_to='quests', verbose_name='баннер квеста'),
            preserve_default=False,
        ),
    ]