# Generated by Django 3.0.5 on 2020-07-09 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_jorang_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jorang',
            name='title',
        ),
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.CharField(default='조랭이의 행복 일기', max_length=100),
        ),
    ]
