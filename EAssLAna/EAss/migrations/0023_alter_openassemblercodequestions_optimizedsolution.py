# Generated by Django 4.0.4 on 2022-06-29 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0022_openassemblercodequestions_checkneededinstructions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openassemblercodequestions',
            name='OptimizedSolution',
            field=models.TextField(blank=True, null=True),
        ),
    ]
