# Generated by Django 3.1.7 on 2021-04-06 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaymentSystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='wallet_number',
            field=models.BigIntegerField(default='1fc2880a-4573-4e16-b933-561681e690d1', primary_key=True, serialize=False),
        ),
    ]
