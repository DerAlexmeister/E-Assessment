# Generated by Django 4.0.4 on 2022-06-26 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0017_openassemblercodequestions_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qawset',
            name='ItemType',
            field=models.CharField(choices=[('None', 'None'), ('MultipleChoice', 'MultipleChoice'), ('SingleChoice', 'SingleChoice'), ('ClozeText', 'ClozeText'), ('TruthTable', 'TruthTable'), ('Calculus', 'Calculus'), ('Assembler', 'Assembler')], default='None', max_length=24),
        ),
    ]