# Generated by Django 4.2.5 on 2024-03-27 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_quiz_submissions_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='submissions_count',
        ),
        migrations.DeleteModel(
            name='UserRank',
        ),
    ]