# Generated by Django 2.1.2 on 2018-10-13 19:51

from django.db import migrations, models
import django.utils.timezone
import universal.fields


class Migration(migrations.Migration):

    dependencies = [
        ('siteuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pontiff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('papal_name', models.CharField(blank=True, max_length=50, null=True)),
                ('begin', models.DateField()),
                ('finish', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='message',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='siteuser',
            name='roles',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]