# Generated by Django 4.0.4 on 2022-07-21 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0020_normalformcorrection_total_points_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normalformcorrection',
            name='total_points',
            field=models.IntegerField(),
        ),
    ]