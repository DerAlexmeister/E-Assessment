# Generated by Django 4.0.4 on 2022-06-16 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0007_gap_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='qawset',
            name='Topic',
            field=models.CharField(choices=[('None', 'None'), ('Computer-Models', 'Computer-Models'), ('Gates', 'Gates'), ('Calculus', 'Calculus'), ('Optimization', 'Optimization'), ('Assembler', 'Assembler'), ('Quantencomputing', 'Quantencomputing')], default='None', max_length=24),
        ),
    ]
