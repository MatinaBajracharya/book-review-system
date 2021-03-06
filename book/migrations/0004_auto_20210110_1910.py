# Generated by Django 3.1.2 on 2021-01-10 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20210110_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdetails',
            name='Book_Author',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='bookdetails',
            name='Book_Title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bookdetails',
            name='ISBN',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='bookdetails',
            name='Image_URL_L',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bookdetails',
            name='Image_URL_M',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bookdetails',
            name='Image_URL_S',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bookdetails',
            name='Publisher',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bookdetails',
            name='Year_Of_Publication',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
