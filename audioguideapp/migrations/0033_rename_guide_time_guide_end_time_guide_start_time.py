# Generated by Django 4.1 on 2023-03-18 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audioguideapp', '0032_guide_charges_guide_guide_date_guide_guide_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guide',
            old_name='guide_time',
            new_name='end_time',
        ),
        migrations.AddField(
            model_name='guide',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
