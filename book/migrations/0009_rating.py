# Generated by Django 3.1.2 on 2021-01-19 14:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_auto_20210111_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('ISBN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.bookdetail')),
            ],
        ),
    ]
