# Generated by Django 4.2.2 on 2023-07-08 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_alter_food_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='category',
            field=models.ManyToManyField(to='food.category'),
        ),
        migrations.AlterField(
            model_name='food',
            name='price',
            field=models.BigIntegerField(),
        ),
    ]
