# Generated by Django 4.0.4 on 2022-06-25 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0013_calculussingleuseranswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculussingleuseranswer',
            name='Question',
            field=models.IntegerField(null=True),
        ),
    ]
