# Generated by Django 2.2.1 on 2019-08-12 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
