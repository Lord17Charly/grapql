# Generated by Django 4.2.13 on 2024-11-12 00:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('header', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='header',
            name='links',
        ),
        migrations.AddField(
            model_name='header',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='header',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='header',
            name='about',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='header',
            name='posted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='header', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='header',
            name='profile_img',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='header',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
