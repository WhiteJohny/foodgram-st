# Generated by Django 5.2.3 on 2025-06-28 20:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_first_name_alter_user_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата подписки'),
            preserve_default=False,
        ),
    ]
