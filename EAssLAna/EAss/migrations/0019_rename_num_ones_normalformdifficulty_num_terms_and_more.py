# Generated by Django 4.0.4 on 2022-07-21 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0018_normalformanswer_normalformquestion_normalformterm_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='normalformdifficulty',
            old_name='num_ones',
            new_name='num_terms',
        ),
        migrations.AlterField(
            model_name='normalformquestion',
            name='normal_form',
            field=models.CharField(choices=[('disjunctive', 'disjunctive'), ('conjunctive', 'conjunctive')], max_length=50),
        ),
        migrations.CreateModel(
            name='NormalFormKnowledge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable_progress', models.FloatField()),
                ('term_progress', models.FloatField()),
                ('difficulty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EAss.normalformdifficulty')),
            ],
        ),
    ]
