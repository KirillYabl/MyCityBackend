# Generated by Django 4.1.6 on 2023-03-16 07:08

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                (
                    'last_login',
                    models.DateTimeField(blank=True, null=True, verbose_name='last login'),
                ),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False,
                        help_text='Designates that this user has all\
                            permissions without explicitly assigning them.',
                        verbose_name='superuser status',
                    ),
                ),
                (
                    'first_name',
                    models.CharField(blank=True, max_length=150, verbose_name='first name'),
                ),
                (
                    'last_name',
                    models.CharField(blank=True, max_length=150, verbose_name='last name'),
                ),
                (
                    'is_staff',
                    models.BooleanField(
                        default=False,
                        help_text='Designates whether the user can log into this admin site.',
                        verbose_name='staff status',
                    ),
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=True,
                        help_text='Designates whether this user should be treated as active.\
                            Unselect this instead of deleting accounts.',
                        verbose_name='active',
                    ),
                ),
                (
                    'date_joined',
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name='date joined',
                    ),
                ),
                (
                    'email',
                    models.EmailField(max_length=254, unique=True, verbose_name='email address'),
                ),
                (
                    'password',
                    models.CharField(
                        max_length=150,
                        validators=[
                            django.core.validators.MinLengthValidator(8),
                            django.core.validators.MaxLengthValidator(20),
                        ],
                        verbose_name='password',
                    ),
                ),
                (
                    'groups',
                    models.ManyToManyField(
                        blank=True,
                        help_text='The groups this user belongs to. A user will get all\
                            permissions granted to each of their groups.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.group',
                        verbose_name='groups',
                    ),
                ),
                (
                    'user_permissions',
                    models.ManyToManyField(
                        blank=True,
                        help_text='Specific permissions for this user.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.permission',
                        verbose_name='user permissions',
                    ),
                ),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                (
                    'full_name',
                    models.CharField(
                        max_length=256,
                        validators=[
                            django.core.validators.RegexValidator(
                                message='ФИО должно содержать обязательно фамилию и имя и\
                                    состоять только из русских букв',
                                regex='^[ёЁа-яА-ЯA-Za-z-]+( [ёЁа-яА-ЯA-Za-z-]+){1,4}$',
                            ),
                        ],
                        verbose_name='ФИО',
                    ),
                ),
                ('birth_date', models.DateField(verbose_name='дата рождения')),
                (
                    'phone',
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region='RU', verbose_name='номер телефона',
                    ),
                ),
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
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=100,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message='в названии команды допускаются русские\
                                    и английские буквы, цифры и пробелы если\
                                        название содержит несколько слов',
                                regex='^[ёЁа-яА-Я!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\\w]+( [ёЁа-яА-Я!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\\w]+)*$',  # noqa: E501
                            ),
                        ],
                        verbose_name='название команды',
                    ),
                ),
                (
                    'captain',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='team',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='капитан',
                    ),
                ),
            ],
            options={
                'verbose_name': 'команда',
                'verbose_name_plural': 'команды',
            },
        ),
        migrations.CreateModel(
            name='TeamMembership',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                (
                    'member_number',
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                        verbose_name='номер участника в команде',
                    ),
                ),
                (
                    'member',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='memberships',
                        to='user_app.member',
                        verbose_name='участник',
                    ),
                ),
                (
                    'team',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='memberships',
                        to='user_app.team',
                        verbose_name='команда',
                    ),
                ),
            ],
            options={
                'verbose_name': 'членство в команде',
                'verbose_name_plural': 'членства в командах',
                'unique_together': {('team', 'member'), ('team', 'member', 'member_number')},
            },
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ManyToManyField(
                related_name='members',
                through='user_app.TeamMembership',
                to='user_app.team',
                verbose_name='команда',
            ),
        ),
    ]
