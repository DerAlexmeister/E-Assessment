# Generated by Django 4.0.4 on 2022-07-07 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0016_normalform_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normalform',
            name='assessment',
            field=models.CharField(choices=[('boolean', 'boolean'), ('grading', 'grading'), ('correcting_boolean', 'correcting_boolean'), ('difference', 'difference')], max_length=50),
        ),
    ]
