# Generated by Django 4.2.13 on 2024-11-13 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work_experiencie', '0004_rename_star_date_workeperiencies_start_date'),
        ('work_exp_archivements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperienciesarchivements',
            name='work_experiencies',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archivements', to='work_experiencie.workeperiencies'),
        ),
    ]
