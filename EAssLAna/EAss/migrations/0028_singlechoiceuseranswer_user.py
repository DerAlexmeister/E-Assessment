# Generated by Django 4.0.4 on 2022-07-10 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0027_openassembleranswer_questionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlechoiceuseranswer',
            name='User',
            field=models.CharField(default='Ben', max_length=1024),
            preserve_default=False,
        ),
    ]
