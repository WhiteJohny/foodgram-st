# Generated by Django 5.2.3 on 2025-06-28 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='measurement_value',
            field=models.FloatField(default=0, verbose_name='Вес/Объем/Количество ингредиента'),
            preserve_default=False,
        ),
    ]
