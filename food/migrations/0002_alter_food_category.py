# Generated by Django 4.2.2 on 2023-07-08 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='food.category'),
        ),
    ]
