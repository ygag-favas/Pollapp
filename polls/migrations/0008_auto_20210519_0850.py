# Generated by Django 3.1.7 on 2021-05-19 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20210519_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='choice_text_ar',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='choice',
            name='choice_text_en',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_text_ar',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_text_en',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
