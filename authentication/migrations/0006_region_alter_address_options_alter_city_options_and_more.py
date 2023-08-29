# Generated by Django 4.2.2 on 2023-08-21 05:40

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_discountcode_province_admin_customer_personnel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='address',
            options={},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'استان', 'verbose_name_plural': 'استان ها'},
        ),
        migrations.RemoveField(
            model_name='address',
            name='province',
        ),
        migrations.RemoveField(
            model_name='city',
            name='province',
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.city'),
        ),
        migrations.AlterField(
            model_name='city',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.DeleteModel(
            name='Province',
        ),
        migrations.AddField(
            model_name='region',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.city'),
        ),
        migrations.AddField(
            model_name='address',
            name='region',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='city', chained_model_field='city', null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.region'),
        ),
    ]