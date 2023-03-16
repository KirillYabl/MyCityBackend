# Generated by Django 4.1.6 on 2023-03-09 20:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(message='ФИО должно содержать обязательно фамилию и имя и состоять только из русских букв', regex='^[ёЁа-яА-ЯA-Za-z-]+( [ёЁа-яА-ЯA-Za-z-]+){1,4}$')], verbose_name='ФИО')),
                ('birth_date', models.DateField(verbose_name='дата рождения')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region='RU', verbose_name='номер телефона')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email')),
                ('is_captain', models.BooleanField(verbose_name='признак капитана')),
            ],
            options={
                'verbose_name': 'участник',
                'verbose_name_plural': 'участники',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='в названии команды допускаются русские и английские буквы, цифры и пробелы если название содержит несколько слов', regex='^[ёЁа-яА-Я\\p{P}\\w]+( [ёЁа-яА-Я\\p{P}\\w]+)*$')], verbose_name='название команды')),
                ('captain', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='team', to=settings.AUTH_USER_MODEL, verbose_name='капитан')),
            ],
            options={
                'verbose_name': 'команда',
                'verbose_name_plural': 'команды',
            },
        ),
        migrations.CreateModel(
            name='TeamMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_number', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='номер участника в команде')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='user_app.member', verbose_name='участник')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='user_app.team', verbose_name='команда')),
            ],
            options={
                'verbose_name': 'членство в команде',
                'verbose_name_plural': 'членства в командах',
            },
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ManyToManyField(related_name='members', through='user_app.TeamMembership', to='user_app.team', verbose_name='команда'),
        ),
    ]