# Generated by Django 3.2.9 on 2022-01-31 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ing',
            name='Value',
            field=models.CharField(max_length=100, null=True, verbose_name='Имя рецепта'),
        ),
        migrations.AddField(
            model_name='ing',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
