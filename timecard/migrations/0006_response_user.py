# Generated by Django 2.0.6 on 2018-08-16 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timecard', '0005_auto_20180816_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='user',
            field=models.CharField(default='blank', max_length=200),
        ),
    ]