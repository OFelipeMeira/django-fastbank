# Generated by Django 4.2.7 on 2023-11-27 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_loaninstallments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='status',
        ),
        migrations.AddField(
            model_name='loan',
            name='payed',
            field=models.BooleanField(default=False),
        ),
    ]
