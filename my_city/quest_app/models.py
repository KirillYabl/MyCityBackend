from django.core.validators import MinValueValidator
from django.db import models
from django.template.defaultfilters import truncatechars


class ContactType(models.Model):
    """Тип контакта нужен, чтобы фронтенд понимал, в какой блок пойдет контакт."""
    name = models.CharField('наименование типа контакта', max_length=64)

    class Meta:
        verbose_name = 'тип контакта'
        verbose_name_plural = 'типы контактов'

    def __str__(self):
        return self.name


class Contact(models.Model):
    """Контакты: соцсети, телефоны, ссылка на политики и т.д. для футера."""
    contact_type = models.ForeignKey(
        verbose_name='тип контакта',
        to=ContactType,
        on_delete=models.PROTECT,
        related_name='types',
    )
    contact = models.TextField('контакт', unique=True)
    description = models.TextField('описание', blank=True)
    order = models.PositiveSmallIntegerField('порядок показа', unique=True, validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'

    def __str__(self):
        return self.contact


class FAQ(models.Model):
    """Часто задаваемые вопросы с ответами."""
    question = models.TextField('вопрос', unique=True)
    answer = models.TextField('ответ')
    order = models.PositiveSmallIntegerField('порядок показа', unique=True, validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'часто задаваемый вопрос'
        verbose_name_plural = 'часто задаваемые вопросы'

    def __str__(self):
        truncate_length = 97  # 100 - 3 (symbols for ellipsis)
        return truncatechars(self.question, truncate_length)
