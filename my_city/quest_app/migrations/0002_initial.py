# Generated by Django 4.1.6 on 2023-03-16 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('quest_app', '0001_initial'),
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='teams',
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name='categories',
                to='user_app.team',
                verbose_name='участвующие команды',
            ),
        ),
        migrations.AddField(
            model_name='assignment',
            name='answer_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='assignments',
                to='quest_app.answertype',
                verbose_name='тип ответа',
            ),
        ),
        migrations.AddField(
            model_name='assignment',
            name='category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='assignments',
                to='quest_app.category',
                verbose_name='категория',
            ),
        ),
        migrations.AddField(
            model_name='answerattempt',
            name='assignment',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='attempts',
                to='quest_app.assignment',
                verbose_name='задание',
            ),
        ),
        migrations.AddField(
            model_name='answerattempt',
            name='team',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='attempts',
                to='user_app.team',
                verbose_name='команда',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={
                ('quest', 'participation_order'),
                ('quest', 'name'),
                ('quest', 'results_order'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together={('category', 'question')},
        ),
        migrations.AlterUniqueTogether(
            name='answerattempt',
            unique_together={('assignment', 'team')},
        ),
    ]
