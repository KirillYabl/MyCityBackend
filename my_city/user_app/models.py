import string

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager

max_password_length = 20
min_password_length = 8


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email address', unique=True)
    password = models.CharField(
        max_length=150,
        verbose_name='password',
        validators=(
            MinLengthValidator(min_password_length),
            MaxLengthValidator(max_password_length),
        ),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email


class Team(models.Model):
    """
    Команда, фактически в рамках сайта почти профиль пользователя, поэтому связь с юзером 1 к 1.

    Решено было не делать команду юзером, потому что регистрируется вроде человек,
    а команда это как бы его профиль.
    """

    name = models.CharField(
        'название команды',
        max_length=100,
        validators=[
            RegexValidator(
                # rus, eng, punctuation, digits signs, splitted with only 1 space
                regex=r'^[ёЁа-яА-Я{punct}\w]+( [ёЁа-яА-Я{punct}\w]+)*$'.format(
                    punct=string.punctuation,
                ),
                message=' '.join(
                    [
                        'в названии команды допускаются русские и английские буквы, цифры',
                        'и пробелы если название содержит несколько слов',
                    ],
                ),
            ),
        ],
        unique=True,
    )
    captain = models.OneToOneField(
        verbose_name='капитан',
        to=User,
        on_delete=models.PROTECT,
        related_name='team',
    )

    class Meta:
        verbose_name = 'команда'
        verbose_name_plural = 'команды'

    def __str__(self):
        return self.name


class Member(models.Model):
    """
    Участники команды.

    Обязательно должны иметь ФИО и дату рождения для того, чтобы сдать документы в мин культуры.
    Номер телефона и емейл обязателен не у всех (в валидаторе создания команды).
    Максимальное количество участников внутри команды будет в промежуточной модели.
    Номер телефона и емейл не делаю уникальными, т.к. команды могут быть новые, а участники
    старые при очередных квестах
    """

    full_name = models.CharField(
        'ФИО',
        max_length=256,
        validators=[
            RegexValidator(
                # words with dash (min 1) split with only 1 space
                regex=r'^[ёЁа-яА-Я-]+( [ёЁа-яА-Я-]+){1,4}$',
                message='ФИО должно содержать обязательно фамилию и имя и состоять \
                    только из русских букв',
            ),
        ],
    )
    birth_date = models.DateField('дата рождения')
    phone = PhoneNumberField('номер телефона', region='RU', blank=True)
    email = models.EmailField('email', blank=True)
    is_captain = models.BooleanField('признак капитана')
    team = models.ForeignKey(
        verbose_name='команда',
        on_delete=models.PROTECT,
        to=Team,
        related_name='members',
    )
    member_number = models.PositiveSmallIntegerField(
        'номер участника в команде',
        validators=[MinValueValidator(1), MaxValueValidator(settings.MAX_MEMBERS_IN_TEAM)],
    )

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'
        unique_together = (('team', 'member_number'),)

    def __str__(self):
        return f'{self.full_name} ({self.birth_date})'
