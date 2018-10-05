# Generated by Django 2.0.6 on 2018-07-06 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteuser', '0002_auto_20180707_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='screen_name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
