# Generated by Django 3.0.5 on 2020-11-19 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HappyWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happy_content', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ReminderWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reminder_content', models.CharField(max_length=200)),
            ],
        ),
    ]
