# Generated by Django 5.0.1 on 2024-01-21 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tttapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
