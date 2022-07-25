# Generated by Django 4.0.4 on 2022-07-10 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0028_singlechoiceuseranswer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='singlechoiceuseranswer',
            name='User',
        ),
        migrations.AddField(
            model_name='calculussingleuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='clozeuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='multiplechoiceuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='openassembleranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='singlechoiceuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='singlefieldclozeuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='singlemultiplechoiceuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='singletruthtableuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='truthtableuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
    ]