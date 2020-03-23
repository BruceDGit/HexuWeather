# Generated by Django 2.1.8 on 2019-11-16 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='用户')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('password_1', models.CharField(max_length=20, verbose_name='密码1')),
                ('password_2', models.CharField(max_length=20, verbose_name='密码2')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]