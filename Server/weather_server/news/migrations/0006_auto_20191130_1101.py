# Generated by Django 2.1.8 on 2019-11-30 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_tjnews_travelnews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sevendaysweather',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
