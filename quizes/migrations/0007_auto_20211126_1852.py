# Generated by Django 2.2 on 2021-11-26 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0006_auto_20211126_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
