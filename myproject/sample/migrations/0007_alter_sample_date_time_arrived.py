# Generated by Django 4.1.5 on 2023-02-03 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0006_alter_sample_date_time_arrived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='date_time_arrived',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
