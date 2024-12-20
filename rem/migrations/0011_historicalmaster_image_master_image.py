# Generated by Django 5.1.4 on 2024-12-13 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rem', '0010_rename_username_client_full_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmaster',
            name='image',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='master',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='masters/'),
        ),
    ]
