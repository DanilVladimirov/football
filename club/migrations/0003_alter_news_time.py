# Generated by Django 3.2.4 on 2021-06-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0002_news_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='time',
            field=models.DateField(auto_now=True),
        ),
    ]
