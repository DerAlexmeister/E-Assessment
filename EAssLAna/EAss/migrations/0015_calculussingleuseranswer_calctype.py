# Generated by Django 4.0.4 on 2022-06-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0014_calculussingleuseranswer_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculussingleuseranswer',
            name='CalcType',
            field=models.CharField(choices=[('None', 'None'), ('Bin', 'Bin'), ('Octa', 'Octa')], default='None', max_length=24),
        ),
    ]