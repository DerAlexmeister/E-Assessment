# Generated by Django 4.0.4 on 2022-07-25 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0042_merge_20220725_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='normalformcorrection',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='normalformguess',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
    ]
