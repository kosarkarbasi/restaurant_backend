# Generated by Django 4.2.2 on 2023-08-09 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('food', '0005_alter_food_category_delete_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('delivery_type', models.CharField(choices=[('send', 'send'), ('onPerson', 'onPerson')], max_length=8)),
                ('address', models.TextField()),
                ('payment_method', models.CharField(choices=[('online', 'online'), ('cash', 'cash'), ('cardReader', 'cardReader')], max_length=10)),
                ('payment_status', models.CharField(choices=[('success', 'success'), ('fail', 'fail')], max_length=7)),
                ('discount_code', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order')),
            ],
        ),
    ]
