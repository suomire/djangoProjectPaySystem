# Generated by Django 3.1.7 on 2021-03-26 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('wallet_number', models.BigIntegerField(default=755036271009, primary_key=True, serialize=False)),
                ('total', models.IntegerField(default=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_amount', models.IntegerField()),
                ('receiver_wallet_number_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='receiver_wallet', to='PaymentSystem.users')),
                ('sender_wallet_number_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='senders_wallet', to='PaymentSystem.users')),
            ],
        ),
    ]
