# Generated by Django 2.1.3 on 2018-11-21 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_book_copies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
