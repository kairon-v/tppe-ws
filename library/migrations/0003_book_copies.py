# Generated by Django 2.1.3 on 2018-11-21 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='copies',
            field=models.IntegerField(default=0),
        ),
    ]