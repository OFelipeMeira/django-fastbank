# Generated by Django 4.2.7 on 2023-12-01 19:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_transfer_receiver_alter_transfer_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]