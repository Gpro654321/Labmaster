# Generated by Django 4.1.5 on 2023-02-03 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0003_alter_sample_sample_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='sample_id',
            field=models.CharField(editable=False, max_length=50, unique=True),
        ),
    ]
