# Generated by Django 2.2.1 on 2019-06-23 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='drive_id',
            field=models.CharField(blank=True, max_length=44, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='drive_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]