# Generated by Django 4.2.5 on 2024-03-27 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_userrank_quizsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='submissions_count',
            field=models.IntegerField(default=0),
        ),
    ]
