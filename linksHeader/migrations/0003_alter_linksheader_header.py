# Generated by Django 4.2.13 on 2024-11-12 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0003_alter_header_posted_by'),
        ('linksHeader', '0002_rename_url_linksheader_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linksheader',
            name='header',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_header', to='header.header'),
        ),
    ]
