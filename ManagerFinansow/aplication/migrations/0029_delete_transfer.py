# Generated by Django 4.1.3 on 2023-02-28 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplication', '0028_alter_transaction_options_alter_transfer_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transfer',
        ),
    ]
