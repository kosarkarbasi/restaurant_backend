# Generated by Django 4.2.2 on 2023-08-09 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_food_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='food.category'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]