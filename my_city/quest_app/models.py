from django.core.validators import MinValueValidator
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from sorl.thumbnail import ImageField

from .querysets import QuestQueryset


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
        related_name='contacts',
    )
    contact = models.TextField('контакт', unique=True)
    description = models.TextField('описание', blank=True)
    order = models.PositiveSmallIntegerField(
        'порядок показа', unique=True, validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'

    def __str__(self):
        return self.contact


class FAQ(models.Model):
    """Часто задаваемые вопросы с ответами."""

    question = models.TextField('вопрос', unique=True)
    answer = models.TextField('ответ')
    order = models.PositiveSmallIntegerField(
        'порядок показа', unique=True, validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'часто задаваемый вопрос'
        verbose_name_plural = 'часто задаваемые вопросы'

    def __str__(self):
        truncate_length = 97  # 100 - 3 (symbols for ellipsis)
        return truncatechars(self.question, truncate_length)


class Quest(models.Model):
    """Квест (по сути мероприятие) с контрольными точками."""

    name = models.CharField('название квеста', max_length=256)
    description = models.TextField('описание', blank=True)
    registration_start_at = models.DateTimeField('начало регистрации')
    start_at = models.DateTimeField('начало квеста')
    end_at = models.DateTimeField('окончание квеста')
    stop_show_at = models.DateTimeField(
        'прекратить показывать',
        help_text='если заполнено, то перестанет отображаться в квестах после этой даты',
        null=True,
        blank=True,
    )
    address = models.CharField('адрес', max_length=256)
    banner = models.ImageField('баннер квеста', upload_to='quests')

    objects = QuestQueryset.as_manager()

    class Meta:
        verbose_name = 'квест'
        verbose_name_plural = 'квесты'

    def __str__(self):
        return f'{self.name} ({self.start_at})'


class Category(models.Model):
    """
    Категория квеста - набор заданий со своими участниками,
    которые не пересекаются с другими категориями.

    Команды заданы через ManyToManyField, заданы к категории, а не к квесту, потому что они
    регистрируются сразу на категорию, а категория однозначно определяет квест, здесь не учтено,
    что нельзя зарегистрироваться в нескольких категориях одного квеста, это будет в API.
    """

    quest = models.ForeignKey(
        verbose_name='квест',
        to=Quest,
        on_delete=models.PROTECT,
        related_name='categories',
    )
    name = models.CharField('название', max_length=128)
    short_description = models.TextField('короткое описание', blank=True)
    long_description = models.TextField('длинное описание', blank=True)
    participation_order = models.PositiveSmallIntegerField(
        'порядок показа категориии для регистрации',
        validators=[MinValueValidator(1)],
    )
    results_order = models.PositiveSmallIntegerField(
        'порядок показа категории в таблице результатов',
        validators=[MinValueValidator(1)],
    )
    teams = models.ManyToManyField(
        verbose_name='участвующие команды',
        to='user_app.Team',
        related_name='categories',
        blank=True,
    )

    class Meta:
        verbose_name = 'категория квеста'
        verbose_name_plural = 'категории квеста'
        unique_together = (
            ('quest', 'name'),
            ('quest', 'participation_order'),
            ('quest', 'results_order'),
        )

    def __str__(self):
        return self.name


class AnswerType(models.Model):
    """Тип ответа."""

    name = models.CharField(
        'наименование типа ответа',
        max_length=64,
        help_text='осторожно, не удаляйте и не добавляйте новые типы ответов без разработчика!',
    )

    class Meta:
        verbose_name = 'тип ответа'
        verbose_name_plural = 'типы ответов'

    def __str__(self):
        return self.name


class Assignment(models.Model):
    """Задание - содержит фото, вопрос, правильный ответ и прочие параметры настройки ответа."""

    category = models.ForeignKey(
        verbose_name='категория',
        to=Category,
        on_delete=models.PROTECT,
        related_name='assignments',
    )
    answer_type = models.ForeignKey(
        verbose_name='тип ответа',
        to=AnswerType,
        on_delete=models.PROTECT,
        related_name='assignments',
    )
    picture = ImageField('картинка для задания', upload_to='assignments')
    question = models.TextField('вопрос')
    answer = models.CharField(
        'правильный ответ',
        max_length=256,
        help_text='если это дата, то указывайте в формате ДД.ММ.ГГГГ',
    )
    is_enumeration = models.BooleanField('признак ответа с перечислением', default=False)
    enumeration_sep = models.CharField(
        'разделитель для перечисления',
        max_length=8,
        default=',',
        help_text='применяется только для ответов с перечислением',
    )
    skip_symbols = models.CharField(
        'символы для пропуска в ответах юзеров',
        max_length=256,
        blank=True,
    )

    class Meta:
        verbose_name = 'задание'
        verbose_name_plural = 'задания'
        unique_together = (('category', 'question'),)

    def __str__(self):
        return self.question


class AnswerAttempt(models.Model):
    """
    Попытка ответа командой.

    Фото, чтобы не занимать много места, будут сжиматься и удаляться через промежуток времени джобом
    Правильность ответа оценивается алгоритмом, но его можно изменить админу превентивно.
    """

    assignment = models.ForeignKey(
        verbose_name='задание',
        to=Assignment,
        on_delete=models.PROTECT,
        related_name='attempts',
    )
    team = models.ForeignKey(
        verbose_name='команда',
        to='user_app.Team',
        on_delete=models.PROTECT,
        related_name='attempts',
    )
    photo = ImageField('фото подтверждение', upload_to='answers', null=True, blank=True)
    answer = models.CharField('ответ', max_length=256)
    created_at = models.DateTimeField('создано', default=timezone.now)
    auto_result = models.BooleanField('результат через алгоритм', db_index=True)
    prevent_result = models.BooleanField(
        'превентивный результат',
        null=True,
        blank=True,
        db_index=True,
        help_text='проставить "да", если после ручной сверки выявлено, что алгоритм ошибся, '
        '"да" или "нет" в этом поле важнее, чем в поле "результат через алгоритм". '
        'Менять правильность ответа нужно именно в этом поле, т.к. поле "результат через алгоритм" '
        'может быть автоматически пересчитано, а это поле нет',
    )
    not_sure = models.BooleanField(
        'признак возможного ложного срабатывания',
        default=False,
        db_index=True,
        help_text='проставляется как "да", если алгоритм не был уверен,\
            что ответ правильный на 100%',
    )

    class Meta:
        verbose_name = 'попытка ответа'
        verbose_name_plural = 'попытки ответов'
        unique_together = (('assignment', 'team'),)

    def __str__(self):
        return f'{self.answer} ({self.created_at})'
