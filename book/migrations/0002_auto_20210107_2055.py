# Generated by Django 3.1.2 on 2021-01-07 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdetails',
            name='Year_Of_Publication',
            field=models.CharField(max_length=100),
        ),
    ]
