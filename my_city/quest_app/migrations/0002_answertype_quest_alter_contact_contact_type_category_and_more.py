# Generated by Django 4.1.6 on 2023-03-11 13:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_alter_team_name_alter_teammembership_unique_together'),
        ('quest_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='осторожно, не удаляйте и не добавляйте новые типы ответов без разработчика!', max_length=64, verbose_name='наименование типа ответа')),
            ],
            options={
                'verbose_name': 'тип ответа',
                'verbose_name_plural': 'типы ответов',
            },
        ),
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='название квеста')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('registration_start_at', models.DateTimeField(verbose_name='начало регистрации')),
                ('start_at', models.DateTimeField(verbose_name='начало квеста')),
                ('end_at', models.DateTimeField(verbose_name='окончание квеста')),
                ('stop_show_at', models.DateTimeField(blank=True, help_text='если заполнено, то перестанет отображаться в квестах после этой даты', null=True, verbose_name='прекратить показывать')),
            ],
            options={
                'verbose_name': 'квест',
                'verbose_name_plural': 'квесты',
            },
        ),
        migrations.AlterField(
            model_name='contact',
            name='contact_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contacts', to='quest_app.contacttype', verbose_name='тип контакта'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='наименование типа контакта')),
                ('short_description', models.TextField(blank=True, verbose_name='короткое описание')),
                ('long_description', models.TextField(blank=True, verbose_name='длинное описание')),
                ('participation_order', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='порядок показа категориии для регистрации')),
                ('results_order', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='порядок показа категории в таблице результатов')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='quest_app.quest', verbose_name='тип контакта')),
                ('teams', models.ManyToManyField(related_name='categories', to='user_app.team', verbose_name='участвующие команды')),
            ],
            options={
                'verbose_name': 'категория квеста',
                'verbose_name_plural': 'категории квеста',
                'unique_together': {('quest', 'participation_order'), ('quest', 'name'), ('quest', 'results_order')},
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', sorl.thumbnail.fields.ImageField(upload_to='assignments', verbose_name='картинка для задания')),
                ('question', models.TextField(verbose_name='вопрос')),
                ('answer', models.CharField(help_text='если это дата, то указывайте в формате ДД.ММ.ГГГГ', max_length=256, verbose_name='правильный ответ')),
                ('is_enumeration', models.BooleanField(default=True, verbose_name='признак ответа с перечислением')),
                ('enumeration_sep', models.CharField(default=',', help_text='применяется только для ответов с перечислением', max_length=8, verbose_name='разделитель для перечисления')),
                ('skip_symbols', models.CharField(max_length=256, verbose_name='символы для пропуска в ответах юзеров')),
                ('answer_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assignments', to='quest_app.answertype', verbose_name='тип ответа')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assignments', to='quest_app.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'задание',
                'verbose_name_plural': 'задания',
                'unique_together': {('category', 'question')},
            },
        ),
        migrations.CreateModel(
            name='AnswerAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='answers', verbose_name='фото подтверждение')),
                ('answer', models.CharField(max_length=256, verbose_name='ответ')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='создано')),
                ('auto_result', models.BooleanField(db_index=True, verbose_name='результат через алгоритм')),
                ('prevent_result', models.BooleanField(blank=True, db_index=True, help_text='проставить "да", если после ручной сверки выявлено, что алгоритм ошибся, "да" или "нет" в этом поле важнее, чем в поле "результат через алгоритм". Менять правильность ответа нужно именно в этом поле, т.к. поле "результат через алгоритм" может быть автоматически пересчитано, а это поле нет', null=True, verbose_name='превентивный результат')),
                ('not_sure', models.BooleanField(db_index=True, default=False, help_text='проставляется как "да", если алгоритм не был уверен, что ответ правильный на 100%', verbose_name='признак возможного ложного срабатывания')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attempts', to='quest_app.assignment', verbose_name='задание')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attempts', to='user_app.team', verbose_name='команда')),
            ],
            options={
                'verbose_name': 'попытка ответа',
                'verbose_name_plural': 'попытки ответов',
                'unique_together': {('assignment', 'team')},
            },
        ),
    ]