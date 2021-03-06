# Generated by Django 4.0.4 on 2022-07-25 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0036_merge_20220721_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculussingleuseranswer',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='calculussingleuseranswer',
            name='Set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EAss.qawset'),
        ),
        migrations.AddField(
            model_name='calculussingleuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='clozeuseranswer',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='clozeuseranswer',
            name='Set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EAss.qawset'),
        ),
        migrations.AddField(
            model_name='clozeuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='gatesanswer',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gatesanswer',
            name='Set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EAss.qawset'),
        ),
        migrations.AddField(
            model_name='gatesanswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='multiplechoiceuseranswer',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='multiplechoiceuseranswer',
            name='Set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EAss.qawset'),
        ),
        migrations.AddField(
            model_name='multiplechoiceuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='openassembleranswer',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='openassembleranswer',
            name='Set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EAss.qawset'),
        ),
        migrations.AddField(
            model_name='openassembleranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='singlechoiceuseranswer',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='singlechoiceuseranswer',
            name='Set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EAss.qawset'),
        ),
        migrations.AddField(
            model_name='singlechoiceuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='singlefieldclozeuseranswer',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='singlefieldclozeuseranswer',
            name='Set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EAss.qawset'),
        ),
        migrations.AddField(
            model_name='singlefieldclozeuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='singlemultiplechoiceuseranswer',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='singlemultiplechoiceuseranswer',
            name='Set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EAss.qawset'),
        ),
        migrations.AddField(
            model_name='singlemultiplechoiceuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='singletruthtableuseranswer',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='singletruthtableuseranswer',
            name='Set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EAss.qawset'),
        ),
        migrations.AddField(
            model_name='singletruthtableuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='truthtableuseranswer',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='truthtableuseranswer',
            name='Set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EAss.qawset'),
        ),
        migrations.AddField(
            model_name='truthtableuseranswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AlterField(
            model_name='qawset',
            name='ItemType',
            field=models.CharField(choices=[('None', 'None'), ('MultipleChoice', 'MultipleChoice'), ('SingleChoice', 'SingleChoice'), ('ClozeText', 'ClozeText'), ('TruthTable', 'TruthTable'), ('Calculus', 'Calculus'), ('Assembler', 'Assembler'), ('Gates', 'Gates')], default='None', max_length=24),
        ),
    ]
