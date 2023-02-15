# Generated by Django 4.1.5 on 2023-02-15 15:34

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('result', '0005_alter_result_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assistant_approval_date', models.DateTimeField(blank=True, null=True)),
                ('associate_approval_date', models.DateTimeField(blank=True, null=True)),
                ('result_content', ckeditor.fields.RichTextField(verbose_name='Result')),
                ('assistant_professor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assistant_approval', to=settings.AUTH_USER_MODEL)),
                ('associate_professor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='associate_approval', to=settings.AUTH_USER_MODEL)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.result')),
            ],
            options={
                'verbose_name': 'Approval',
            },
        ),
    ]
