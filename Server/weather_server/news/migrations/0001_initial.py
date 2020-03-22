# Generated by Django 2.1.8 on 2019-11-20 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FutureWeather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=20, verbose_name='省份')),
                ('city', models.CharField(max_length=20, verbose_name='城市')),
                ('district', models.CharField(max_length=20, verbose_name='区')),
                ('date', models.CharField(max_length=50, verbose_name='日期')),
                ('week', models.CharField(max_length=10, verbose_name='星期')),
                ('temperature', models.IntegerField(verbose_name='温度')),
                ('weather', models.CharField(max_length=20, verbose_name='天气')),
                ('wind', models.CharField(max_length=20, verbose_name='风力等级')),
            ],
            options={
                'db_table': 'future_weather',
            },
        ),
        migrations.CreateModel(
            name='RealtimeWeather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=20, verbose_name='省份')),
                ('city', models.CharField(max_length=20, verbose_name='城市')),
                ('district', models.CharField(max_length=20, verbose_name='区')),
                ('temperature', models.IntegerField(verbose_name='温度')),
                ('t_date', models.DateField(verbose_name='日期')),
                ('get_week', models.CharField(max_length=10, verbose_name='具体星期')),
                ('time', models.TimeField(verbose_name='时间')),
            ],
            options={
                'db_table': 'realtine_weather',
            },
        ),
        migrations.CreateModel(
            name='TodayWeather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=20, verbose_name='省份')),
                ('city', models.CharField(max_length=20, verbose_name='城市')),
                ('district', models.CharField(max_length=20, verbose_name='区')),
                ('place', models.CharField(max_length=50, verbose_name='地点')),
                ('date', models.CharField(max_length=50, verbose_name='日期')),
                ('week', models.CharField(max_length=10, verbose_name='星期')),
                ('temperature', models.IntegerField(verbose_name='温度')),
                ('weather', models.CharField(max_length=20, verbose_name='天气')),
                ('wind', models.CharField(max_length=20, verbose_name='风力等级')),
                ('dressing_index', models.CharField(max_length=100, verbose_name='穿衣指数')),
                ('uv_index', models.CharField(max_length=20, verbose_name='紫外线指数')),
                ('wash_index', models.CharField(max_length=20, verbose_name='洗衣指数')),
                ('pm_index', models.CharField(max_length=20, verbose_name='pm指数')),
            ],
            options={
                'db_table': 'today_weather',
            },
        ),
    ]
