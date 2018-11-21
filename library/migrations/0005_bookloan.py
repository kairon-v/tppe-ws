# Generated by Django 2.1.3 on 2018-11-21 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20181121_0244'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookLoan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_date', models.DateField(auto_now=True)),
                ('days', models.IntegerField(default=0)),
                ('return_date', models.DateField(null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='library.User')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='library.User')),
            ],
        ),
    ]
