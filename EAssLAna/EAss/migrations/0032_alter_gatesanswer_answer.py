# Generated by Django 4.0.4 on 2022-07-20 22:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0031_rename_circuitfunction_gatesanswer_expectedcircuitfunction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gatesanswer',
            name='Answer',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
    ]